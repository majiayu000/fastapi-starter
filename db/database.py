from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = (
    "postgresql+psycopg://postgres:123456@localhost:5432/sys"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 每个实例化的 SessionLocal 对象都是一个数据库会话。Session 类的实例不是线程安全的，因此最好在每个请求中创建一个实例，并在请求结束时关闭它。
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 类将在 models.py 文件中用于创建每个数据库模型或类
Base = declarative_base()