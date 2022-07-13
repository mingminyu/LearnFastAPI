# coding: utf8
# ===================================
# Author: yumingmin
# File: database.py
# Cate: FastAPI
# Create time: 2022/7/8 10:31
# Update time: 
# ===================================

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_SQLITE_DATABASE_URL = "sqlite:///./coronavirus.sqlite3"
# POSTGRESQL 和 MySQL 的连接方式
SQLALCHEMY_POSTGRESQL_DATABASE_URL = "postgresql://username:password@host:port/db_name"

# `echo=True` 表示引擎蒋使用 `repr` 函数记录所有语句及其参数列表到日志
# 由于 SQLAlchemy 是多线程的，指定 `check_same_thread=False` 来让建议的对象任意线程都可以使用
# 这个参数只在 SQLite 数据库时设置
engine = create_engine(
    SQLALCHEMY_SQLITE_DATABASE_URL,
    encoding="utf-8",
    echo=True,
    connect_args={"check_same_thread": False}
)

# 在 SQLAlchemy 中，CRUD 都是通过会话(session) 进行的，所以我们必须要先创建会话，每一个 SessionLocal 实例就是一个数据库 session
# `flush` 是指发送数据库语句到数据库中，但数据库不一定执行写入磁盘
# `commit` 是指提交事物，将变更保存到数据库文件
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=True)

# 创建基本映射类
Base = declarative_base(bind=engine, name="Base")
