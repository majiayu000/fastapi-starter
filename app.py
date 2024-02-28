from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy import create_engine
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from db import SessionLocal, engine
import crud, models, schemas
from sqlalchemy.orm import Session
from api import api_router
from fastapi.middleware.cors import CORSMiddleware
from worker import celery_app, add

models.Base.metadata.create_all(bind=engine)
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


@app.get("/task")
async def process_endpoint():
    result = add.delay(1,2)
    return {"task_id": result.id}


app.include_router(api_router)