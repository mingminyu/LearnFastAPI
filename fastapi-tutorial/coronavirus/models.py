# coding: utf8
# ===================================
# Author: yumingmin
# File: models.py
# Cate: FastAPI
# Create time: 2022/7/8 10:31
# Update time: 
# ===================================

"""SQLAlchemy 教程
* SQLAlchemy 基本操作：http://www.taodudu.cc/news/show-175725.html
* Python3+SQLAlchemy+SQLite 实现 ORM 教程：https://www.cnblogs.com/jiangxiaobo/p/12350561.html
* SQLAlchemy 基本知识 Autoflush 和 Autocommit: https://zhuanlan.zhihu.com/p/48994990
"""

from sqlalchemy import Column, String, Integer, BigInteger, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from .database import Base


class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    province = Column(String(100), unique=True, nullable=False, comment="省/直辖市")
    country = Column(String(100), nullable=False, comment="国家")
    country_code = Column(String(100), nullable=False, comment="国家代码")
    country_population = Column(String(100), nullable=False, comment="国家人口")
    data = relationship('Data', back_populates="city")
    create_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    update_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # __mapper_args__ = {"order_by": country_code}

    def __repr__(self):
        return f"{self.country}-{self.province}"


class Data(Base):
    __tablename__ = "data"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey("city.id"), comment="所属省/直辖市")
    date = Column(Date, nullable=False, comment="数据日期")
    confirmed = Column(BigInteger, default=0, nullable=False, comment="确诊数量")
    deaths = Column(BigInteger, default=0, nullable=False, comment="死亡数量")
    recovered = Column(BigInteger, default=0, nullable=False, comment="痊愈数量")
    # `City` 是关联的类名，back_populates 来指定反向访问的属性名称
    city = relationship("City", back_populates="data")
    create_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    update_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # __mapper_args__ = {"order_by": date.desc()}

    def __repr__(self):
        return f"{repr(self.date)}: 确诊 {self.confirmed} 例"
