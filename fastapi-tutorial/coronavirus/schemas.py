# coding: utf8
# ===================================
# Author: yumingmin
# File: schemas.py
# Cate: FastAPI
# Create time: 2022/7/8 10:32
# Update time: 
# ===================================

from datetime import date, datetime
from pydantic import BaseModel


class CreateData(BaseModel):
    date: date
    confirmed: int = 0
    deaths: int = 0
    recovered: int = 0


class ReadData(BaseModel):
    id: int
    city_id: int
    create_at: datetime
    update_at: datetime

    class Config:
        orm_mode = True


class CreateCity(BaseModel):
    province: str
    country: str
    country_code: str
    country_population: int


class ReadCity(BaseModel):
    id: int
    create_at: datetime
    update_at: datetime

    class Config:
        orm_mode = True
