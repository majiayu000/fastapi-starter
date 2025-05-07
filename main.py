from fastapi import FastAPI, HTTPException, Depends, status
from api import api_router
from fastapi.middleware.cors import CORSMiddleware


# models.Base.metadata.create_all(bind=engine)
# 创建 FastAPI 实例
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，或者指定特定来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)


# 创建一个路由来返回数据
@app.get("/hi")
async def read_data():
    return "hello world"


app.include_router(api_router)
