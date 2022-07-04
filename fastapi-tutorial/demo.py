# coding: utf8
# ==================================
# Author: yumingmin
# Cate: FastAPI
# Create Time: 2022/07/04 14:33:01
# Update Time:
# ===================================

"""
# 启动命令: uvicorn main:app --reload
"""

from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


class CityInfo(BaseModel):
    """
    使用 Optional 时可以不传具体值，默认是 null
    """
    province: str
    country: str
    is_affected: Optional[bool] = None


@app.get("/")
async def hello_world():
    return {"hello": "world"}


# 带参数以及查询参数的请求
@app.get("/city/{city}")
async def result(city: str, query_string: Optional[str] = None):
    return {"city": city, "query_string": query_string}


@app.put("/city/{city}")
async def result(city: str, city_info: CityInfo):
    return {"city": city, "country": city_info.country, "is_affected": city_info.is_affected}
