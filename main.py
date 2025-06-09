from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from api import api_router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from common.startup_banner import print_banner, print_startup_tips
from common.log import EnhancedLog
from config.app_config import get_config, get_service_port, get_current_env


# models.Base.metadata.create_all(bind=engine)
# 创建 FastAPI 实例
app = FastAPI(
    title="FastAPI Starter",
    description="🚀 现代化的 Python Web API 框架",
    version="1.0.0",
)

# 配置模板和静态文件
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，或者指定特定来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)


# 启动页面路由
@app.get("/", response_class=HTMLResponse)
async def welcome_page(request: Request):
    """
    FastAPI 启动欢迎页面
    """
    logger = EnhancedLog.get_logger("api")
    client_ip = request.client.host
    user_agent = request.headers.get("user-agent", "Unknown")

    logger.info(
        "🚀 访问欢迎页面",
        extra={
            "extra_fields": {
                "client_ip": client_ip,
                "user_agent": user_agent,
                "endpoint": "/",
                "method": "GET",
            }
        },
    )

    return templates.TemplateResponse("index.html", {"request": request})


# 创建一个路由来返回数据
@app.get("/hi")
async def read_data():
    logger = EnhancedLog.get_logger("api")
    logger.info(
        "🚀 测试接口被调用",
        extra={"extra_fields": {"endpoint": "/hi", "method": "GET"}},
    )
    return "hello world"


app.include_router(api_router)


if __name__ == "__main__":
    # 加载配置
    config = get_config()
    port = get_service_port()
    env = get_current_env()

    # 初始化日志系统
    app_logger = EnhancedLog.get_logger("app")

    print_banner(port)
    print_startup_tips(port)

    app_logger.info(f"🚀 FastAPI应用启动 | 环境: {env} | 端口: {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
