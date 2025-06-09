#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FastAPI Starter 启动横幅模块
显示艺术字和项目信息
"""

import os
from datetime import datetime


def print_banner(port: int = 8090):
    """打印启动横幅

    Args:
        port: 服务端口号
    """

    # 清屏（可选）
    # os.system('clear' if os.name == 'posix' else 'cls')

    # 彩色输出支持 - 现代配色
    class Colors:
        BLUE = "\033[94m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        RED = "\033[91m"
        PURPLE = "\033[95m"
        CYAN = "\033[96m"
        WHITE = "\033[97m"
        BOLD = "\033[1m"
        UNDERLINE = "\033[4m"
        END = "\033[0m"
        # 新增现代配色
        ELECTRIC_BLUE = "\033[38;2;0;212;255m"
        NEON_GREEN = "\033[38;2;0;255;136m"
        HOT_PINK = "\033[38;2;255;107;157m"
        BRIGHT_ORANGE = "\033[38;2;255;170;0m"
        DIM_WHITE = "\033[38;2;200;200;200m"

    # FastAPI 艺术字 - 现代配色
    ascii_art = f"""{Colors.ELECTRIC_BLUE}{Colors.BOLD}
███████╗ █████╗ ███████╗████████╗ █████╗ ██████╗ ██╗
██╔════╝██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██║
█████╗  ███████║███████╗   ██║   ███████║██████╔╝██║
██╔══╝  ██╔══██║╚════██║   ██║   ██╔══██║██╔═══╝ ██║
██║     ██║  ██║███████║   ██║   ██║  ██║██║     ██║
╚═╝     ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝     ╚═╝
{Colors.END}"""

    # 项目信息 - 现代配色
    project_info = f"""
{Colors.DIM_WHITE}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                    {Colors.ELECTRIC_BLUE}{Colors.BOLD}FastAPI Starter Project{Colors.END}{Colors.DIM_WHITE}                    ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ {Colors.HOT_PINK}⚡ 框架:{Colors.END}     FastAPI - 现代化的高性能Web框架                  ┃
┃ {Colors.HOT_PINK}🚀 特性:{Colors.END}     异步处理、自动文档生成、类型提示                 ┃
┃ {Colors.HOT_PINK}📖 文档:{Colors.END}     http://localhost:{port}/docs                       ┃
┃ {Colors.HOT_PINK}🔧 管理:{Colors.END}     http://localhost:{port}/redoc                      ┃
┃ {Colors.HOT_PINK}🏠 首页:{Colors.END}     http://localhost:{port}/                           ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ {Colors.BRIGHT_ORANGE}🕐 启动时间:{Colors.END} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                              ┃
┃ {Colors.BRIGHT_ORANGE}🔧 运行环境:{Colors.END} Python {os.sys.version.split()[0]}                                    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{Colors.END}
"""

    # 启动状态 - 现代配色
    status_line = f"""
{Colors.DIM_WHITE}{'='*60}{Colors.END}
{Colors.NEON_GREEN}{Colors.BOLD}🟢 服务启动成功！正在监听 http://0.0.0.0:{port}{Colors.END}
{Colors.DIM_WHITE}{'='*60}{Colors.END}
"""

    # 输出所有内容
    print(ascii_art)
    print(project_info)
    print(status_line)


def print_startup_tips(port: int = 8090):
    """打印启动提示

    Args:
        port: 服务端口号
    """

    class Colors:
        BLUE = "\033[94m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        CYAN = "\033[96m"
        WHITE = "\033[97m"
        BOLD = "\033[1m"
        END = "\033[0m"
        # 现代配色
        ELECTRIC_BLUE = "\033[38;2;0;212;255m"
        NEON_GREEN = "\033[38;2;0;255;136m"
        HOT_PINK = "\033[38;2;255;107;157m"
        BRIGHT_ORANGE = "\033[38;2;255;170;0m"
        DIM_WHITE = "\033[38;2;200;200;200m"

    tips = f"""
{Colors.ELECTRIC_BLUE}{Colors.BOLD}💡 快速开始提示:{Colors.END}
{Colors.DIM_WHITE}• 访问 {Colors.HOT_PINK}http://localhost:{port}/{Colors.END}{Colors.DIM_WHITE} 查看欢迎页面{Colors.END}
{Colors.DIM_WHITE}• 访问 {Colors.HOT_PINK}http://localhost:{port}/docs{Colors.END}{Colors.DIM_WHITE} 查看交互式API文档{Colors.END}
{Colors.DIM_WHITE}• 访问 {Colors.HOT_PINK}http://localhost:{port}/hi{Colors.END}{Colors.DIM_WHITE} 测试基础接口{Colors.END}
{Colors.DIM_WHITE}• 按 {Colors.NEON_GREEN}Ctrl+C{Colors.END}{Colors.DIM_WHITE} 停止服务{Colors.END}

{Colors.NEON_GREEN}Happy coding! 🎉{Colors.END}
"""
    print(tips)


if __name__ == "__main__":
    port = 8090  # 默认端口
    print_banner(port)
    print_startup_tips(port)
