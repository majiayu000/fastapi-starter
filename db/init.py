from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .database import Base  

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建表格
Base.metadata.create_all(bind=engine)