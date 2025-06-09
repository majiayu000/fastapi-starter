#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版日志系统 - 融合多进程安全与智能内容处理
支持内容截断、统一日志、Socket连接、自动归档等高级特性
"""

import logging
import logging.handlers
import os
import sys
import time
import shutil
import functools
import re
import socket
import json
import threading
from datetime import datetime, timedelta, time as dt_time
from functools import wraps
from pathlib import Path
from typing import Any, Callable, TypeVar, Optional, Dict
from enum import Enum

F = TypeVar("F", bound=Callable[..., Any])

# 尝试导入多进程安全的日志处理器
try:
    from concurrent_log_handler import ConcurrentRotatingFileHandler

    CONCURRENT_HANDLER_AVAILABLE = True
except ImportError:
    CONCURRENT_HANDLER_AVAILABLE = False


class LogLevel(str, Enum):
    """日志级别枚举"""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


def _truncate_large_content(obj, max_length=1000, base64_max_length=100, key_path=""):
    """截断日志中的大型内容，特别是base64编码的内容"""
    sensitive_keys = [
        "image",
        "base64",
        "file",
        "content",
        "body",
        "data",
        "password",
        "token",
    ]
    base64_pattern = re.compile(r"^[A-Za-z0-9+/]{50,}={0,2}$")
    is_sensitive = any(key in key_path.lower() for key in sensitive_keys)
    effective_max_length = base64_max_length if is_sensitive else max_length

    if isinstance(obj, dict):
        result = {}
        for key, value in obj.items():
            new_key_path = f"{key_path}.{key}" if key_path else key
            result[key] = _truncate_large_content(
                value, max_length, base64_max_length, new_key_path
            )
        return result
    elif isinstance(obj, list):
        return [
            _truncate_large_content(item, max_length, base64_max_length, key_path)
            for item in obj
        ]
    elif isinstance(obj, str):
        if base64_pattern.match(obj) and len(obj) > base64_max_length:
            return f"{obj[:base64_max_length]}... [截断,总长度:{len(obj)}字节]"
        elif obj.strip().startswith("{") and obj.strip().endswith("}"):
            try:
                json_obj = json.loads(obj)
                if isinstance(json_obj, dict) and len(obj) > effective_max_length:
                    return json.dumps(
                        _truncate_large_content(json_obj, max_length, base64_max_length)
                    )
            except:
                pass
        if len(obj) > effective_max_length:
            return f"{obj[:effective_max_length]}... [截断,总长度:{len(obj)}字符]"
        return obj
    else:
        return obj


class EnhancedLog:
    """增强版日志管理器 - 融合多进程安全与智能内容处理"""

    dir_name: str = "logs"
    _service_name: str = None
    _use_socket_handler: bool = False
    _log_server_host: str = "localhost"
    _log_server_port: int = 9020
    _loggers: Dict[str, logging.Logger] = {}

    @classmethod
    def get_service_name(cls) -> str:
        """获取服务名称"""
        if cls._service_name is None:
            cls._service_name = os.getenv("SERVICE_NAME", "fastapi-starter")
        return cls._service_name

    @classmethod
    def is_multiprocess_environment(cls) -> bool:
        """检测是否在多进程环境中"""
        workers = int(os.getenv("WEB_CONCURRENCY", "1"))
        uvicorn_workers = int(os.getenv("UVICORN_WORKERS", "1"))
        return workers > 1 or uvicorn_workers > 1

    @classmethod
    def get_logger(
        cls, module_name: str = None, file_name: str = None, **kwargs
    ) -> logging.Logger:
        """获取增强的日志记录器"""
        logger_key = f"{module_name or 'default'}_{file_name or 'app'}"

        if logger_key not in cls._loggers:
            cls._loggers[logger_key] = cls._create_enhanced_logger(
                module_name or "app",
                file_name or "app.log",
                kwargs.get("multiprocess_safe", cls.is_multiprocess_environment()),
            )

        logger = cls._loggers[logger_key]

        # 返回模块适配器
        if module_name:

            class ModuleAdapter(logging.LoggerAdapter):
                def process(self, msg, kwargs):
                    if "extra" not in kwargs:
                        kwargs["extra"] = {}
                    kwargs["extra"]["module_source"] = module_name
                    kwargs["extra"]["service_name"] = cls.get_service_name()
                    return msg, kwargs

            return ModuleAdapter(logger, {})

        return logger

    @classmethod
    def _create_enhanced_logger(
        cls, name: str, file_name: str, multiprocess_safe: bool
    ) -> logging.Logger:
        """创建增强的日志器"""
        logging.Formatter.converter = lambda *args: datetime.now().timetuple()

        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        logger.propagate = False
        logger.handlers.clear()

        # 创建格式化器
        formatter = cls._create_formatter()

        # 控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # 文件处理器
        cls._setup_file_handlers(logger, file_name, formatter, multiprocess_safe)

        return logger

    @classmethod
    def _create_formatter(cls):
        """创建增强的格式化器"""

        class CustomFormatter(logging.Formatter):
            def __init__(self):
                fmt = "%(asctime)s.%(msecs)03d │ %(service_name)-12s │ %(levelname)-7s │ %(module)-15.15s │ %(funcName)-20.20s │ %(lineno)4d │ %(message)s"
                super().__init__(fmt=fmt, datefmt="%Y-%m-%d %H:%M:%S")

            def format(self, record):
                # 处理消息内容截断
                if hasattr(record, "msg"):
                    if isinstance(record.msg, dict):
                        record.msg = _truncate_large_content(record.msg)
                    elif isinstance(record.msg, str) and len(record.msg) > 1000:
                        record.msg = _truncate_large_content(record.msg)

                # 确保service_name存在
                if not hasattr(record, "service_name"):
                    record.service_name = cls.get_service_name()

                # 添加emoji
                msg = str(record.msg)
                if "执行时间" in msg and not msg.startswith("✅"):
                    record.msg = f"✅ {msg.replace('执行时间:', 'took')}"
                elif (
                    "initialized" in msg.lower() or "started" in msg.lower()
                ) and not msg.startswith("✅"):
                    record.msg = f"✅ {msg}"
                elif record.levelno >= logging.ERROR and not msg.startswith("❌"):
                    record.msg = f"❌ {msg}"
                elif record.levelno == logging.WARNING and not msg.startswith("❗️"):
                    record.msg = f"❗️ {msg}"

                return super().format(record)

        return CustomFormatter()

    @classmethod
    def _setup_file_handlers(
        cls, logger: logging.Logger, file_name: str, formatter, multiprocess_safe: bool
    ):
        """设置文件处理器"""
        log_dir = Path(cls.dir_name)
        log_dir.mkdir(exist_ok=True)

        # 主日志文件
        log_file_path = log_dir / file_name

        if multiprocess_safe and CONCURRENT_HANDLER_AVAILABLE:
            file_handler = ConcurrentRotatingFileHandler(
                str(log_file_path),
                maxBytes=10 * 1024 * 1024,
                backupCount=30,
                encoding="utf-8",
            )
        else:
            file_handler = logging.handlers.TimedRotatingFileHandler(
                str(log_file_path),
                when="midnight",
                interval=1,
                backupCount=30,
                encoding="utf-8",
                atTime=dt_time(0, 0, 0),
            )

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # 错误日志文件
        error_file_path = log_dir / f"{file_name.replace('.log', '_error.log')}"

        if multiprocess_safe and CONCURRENT_HANDLER_AVAILABLE:
            error_handler = ConcurrentRotatingFileHandler(
                str(error_file_path),
                maxBytes=10 * 1024 * 1024,
                backupCount=30,
                encoding="utf-8",
            )
        else:
            error_handler = logging.handlers.TimedRotatingFileHandler(
                str(error_file_path),
                when="midnight",
                interval=1,
                backupCount=30,
                encoding="utf-8",
                atTime=dt_time(0, 0, 0),
            )

        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        logger.addHandler(error_handler)


# 向后兼容的Log类
Log = EnhancedLog


def log_time(logger: logging.Logger) -> Callable[[F], F]:
    """执行时间装饰器"""

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed_time = (time.time() - start_time) * 1000
            logger.debug(f"{func.__name__} 执行时间: {elapsed_time:.2f} ms")
            return result

        return wrapper

    return decorator


def log_request(func):
    """请求日志装饰器"""
    logger = EnhancedLog.get_logger("request")

    @functools.wraps(func)
    def wrapper(self, request, *args, **kwargs):
        start_time = time.time()
        method = request.method
        path = request.get_full_path()

        logger.info(f"Received {method} request for {path}")

        try:
            response = func(self, request, *args, **kwargs)
            duration = (time.time() - start_time) * 1000
            logger.info(f"Completed {method} request for {path} in {duration:.2f}ms")
            return response
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            logger.error(
                f"Failed {method} request for {path} in {duration:.2f}ms: {str(e)}"
            )
            raise

    return wrapper


# 便捷的全局logger实例
logger = EnhancedLog.get_logger("request")
