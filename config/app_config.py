#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用配置管理模块
从 config.ini 文件读取配置信息
"""

import os
import configparser
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class AppConfig:
    """应用配置数据类"""

    # 服务配置
    service_port: int = 8080
    typo_port: int = 4781

    # 数据库配置
    host: Optional[str] = None
    port: Optional[int] = None
    user: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None

    # 服务发现配置
    server_addresses: Optional[str] = None
    namespace: Optional[str] = None

    # Elasticsearch配置
    elasticsearch_host: Optional[str] = None
    elasticsearch_port: Optional[int] = None

    # 应用配置
    prefix: str = "app"
    disable_rocketmq: bool = True
    inner_url: Optional[str] = None

    # LLM配置
    default_timeout: int = 10
    image_timeout: int = 15
    time_out_fixed: int = 30
    default_model: str = "azure-gpt4o"
    model_backup: str = "gpt-4.1"

    # 环境配置
    environment: str = "DEMO"


class ConfigManager:
    """配置管理器"""

    def __init__(self, config_file: str = "config/config.ini"):
        self.config_file = Path(config_file)
        self.config = configparser.ConfigParser()
        self._app_config: Optional[AppConfig] = None
        self._load_config()

    def _load_config(self):
        """加载配置文件"""
        if not self.config_file.exists():
            raise FileNotFoundError(f"配置文件不存在: {self.config_file}")

        try:
            self.config.read(self.config_file, encoding="utf-8")
        except Exception as e:
            raise Exception(f"读取配置文件失败: {e}")

    def get_current_env(self) -> str:
        """获取当前环境"""
        # 优先从环境变量获取
        env_from_var = os.getenv("APP_ENV")
        if env_from_var:
            return env_from_var.upper()

        # 从配置文件获取
        if self.config.has_section("ENV") and self.config.has_option("ENV", "ENV"):
            return self.config.get("ENV", "ENV").upper()

        return "DEMO"  # 默认环境

    def get_app_config(self) -> AppConfig:
        """获取应用配置"""
        if self._app_config is None:
            self._app_config = self._build_app_config()
        return self._app_config

    def _build_app_config(self) -> AppConfig:
        """构建应用配置"""
        env = self.get_current_env()

        if not self.config.has_section(env):
            raise Exception(f"配置文件中没有找到环境 [{env}] 的配置")

        section = self.config[env]

        # 构建配置对象
        config = AppConfig()
        config.environment = env

        # 服务配置
        config.service_port = section.getint("SERVICE_PORT", fallback=8080)
        config.typo_port = section.getint("TYPO_PORT", fallback=4781)

        # 数据库配置
        config.host = section.get("HOST", fallback=None)
        config.port = (
            section.getint("PORT", fallback=None) if section.get("PORT") else None
        )
        config.user = section.get("USER", fallback=None)
        config.password = section.get("PASSWORD", fallback=None)
        config.name = section.get("NAME", fallback=None)

        # 服务发现配置
        config.server_addresses = section.get("SERVER_ADDRESSES", fallback=None)
        config.namespace = section.get("NAMESPACE", fallback=None)

        # Elasticsearch配置
        config.elasticsearch_host = section.get("ELASTICSEARCH_HOST", fallback=None)
        config.elasticsearch_port = (
            section.getint("ELASTICSEARCH_PORT", fallback=None)
            if section.get("ELASTICSEARCH_PORT")
            else None
        )

        # 应用配置
        config.prefix = section.get("PREFIX", fallback="app")
        config.disable_rocketmq = section.getboolean("DISABLE_ROCKETMQ", fallback=True)
        config.inner_url = section.get("INNER_URL", fallback=None)

        # LLM配置
        config.default_timeout = section.getint("DEFAULT_TIMEOUT", fallback=10)
        config.image_timeout = section.getint("IMAGE_TIMEOUT", fallback=15)
        config.time_out_fixed = section.getint("TIME_OUT_FIXED", fallback=30)
        config.default_model = section.get("DEFAULT_MODEL", fallback="azure-gpt4o")
        config.model_backup = section.get("MODEL_BACKUP", fallback="gpt-4.1")

        return config

    def get_config_value(self, section: str, key: str, fallback: Any = None) -> Any:
        """获取指定配置值"""
        if not self.config.has_section(section):
            return fallback

        return self.config.get(section, key, fallback=fallback)

    def get_all_config(self) -> Dict[str, Dict[str, str]]:
        """获取所有配置"""
        result = {}
        for section_name in self.config.sections():
            result[section_name] = dict(self.config[section_name])
        return result

    def reload_config(self):
        """重新加载配置"""
        self._app_config = None
        self._load_config()

    def print_current_config(self):
        """打印当前配置信息"""
        config = self.get_app_config()
        env = self.get_current_env()

        print(f"""
🔧 当前配置信息:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 环境: {env}
🌐 服务端口: {config.service_port}
🔍 Typo端口: {config.typo_port}
📊 Elasticsearch: {config.elasticsearch_host}:{config.elasticsearch_port}
🚀 服务前缀: {config.prefix}
🤖 默认模型: {config.default_model}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """)


# 全局配置管理器实例
config_manager = ConfigManager()


def get_config() -> AppConfig:
    """获取应用配置的便捷函数"""
    return config_manager.get_app_config()


def get_service_port() -> int:
    """获取服务端口的便捷函数"""
    return config_manager.get_app_config().service_port


def get_current_env() -> str:
    """获取当前环境的便捷函数"""
    return config_manager.get_current_env()


# 如果作为主模块运行，打印配置信息
if __name__ == "__main__":
    print("🚀 FastAPI Starter 配置管理")

    try:
        config_manager.print_current_config()

        # 打印所有可用环境
        all_configs = config_manager.get_all_config()
        print("\n📋 所有可用环境:")
        for section in all_configs.keys():
            if section != "ENV":
                port = config_manager.get_config_value(
                    section, "SERVICE_PORT", "未配置"
                )
                print(f"   • {section}: 端口 {port}")

    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
