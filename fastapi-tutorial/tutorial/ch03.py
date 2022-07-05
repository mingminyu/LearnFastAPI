# coding: utf8
# ================================
# Author: yumingmin
# Cate: FastAPI
# Create Time: 2022/7/4 18:31:00
# Update Time:
# ================================
"""路径参数和数字验证 (Path Parameters and Number Validations)
- 函数的顺序就是路由的顺序
- 当请求为 /path/parameters 时，哪个函数在前就匹配哪个
"""
from typing import Optional

from fastapi import APIRouter, Path
from enum import Enum

app03 = APIRouter()


@app03.get("/path/{parameters}")
async def path_params01(parameters: str):
    return {"message": parameters}


@app03.get("/path/parameters")
async def path_params01():
    return {"message": "This is a message!"}


class CityName(str, Enum):
    Beijing = "Beijing China"
    Shanghai = "Shanghai China"


@app03.get("/enum/{city}")
async def latest(city: CityName):
    if city == CityName.Shanghai:
        return {"city_name": city, "confirmed": 1492, "death": 7}

    if city == CityName.Beijing:
        return {"city_name": city, "confirmed": 1201, "death": 10}

    return {"city_name": city, "latest": "unknown"}


# 加上 path 则可以接收 Linux 路径
@app03.get("/files/{file_path:path}")
async def filepath(file_path: str):
    return f"The file path is  {file_path}"


# Path(...) 中的 3 个点号表示必填
@app03.get("/path2/{num}")
async def path_params_validate(
        num: int = Path(..., ge=1, le=10, title="Your number", description="输入文件夹数字"),
):
    return num


"""查询参数和字符串验证(Query Parameters and String Validations)

"""


@app03.get("/query")
async def page_limit(page: int = 1, limit: Optional[int] = None):
    if limit:
        return {"page": page, "limit": limit}

    return {"page": page}


@app03.get("/query/bool/conversion")
async def type_conversion(param: bool = False):
    """传入的如果是 TRUE / FALSE / true / false / 0 / 1 都可以正常被解析
    如果传入的非上面值，则会报错
    """
    return param

