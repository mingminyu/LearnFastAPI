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
from datetime import date
from enum import Enum
from typing import Optional, List
from fastapi import APIRouter, Path, Query, Cookie, Header
from pydantic import BaseModel, Field

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

# bool 类型参数

如果传入的如果是 TRUE / FALSE / true / false / 0 / 1 / yes / no 都会被转换成 true / false
"""


@app03.get("/query")
async def page_limit(page: int = 1, limit: Optional[int] = None):
    if limit:
        return {"page": page, "limit": limit}

    return {"page": page}


@app03.get("/query/bool/conversion")
async def type_conversion(param: bool = False):
    """
    如果传入的非上面值，则会报错
    """
    return param


@app03.get("/query/validations")
async def query_params_validate(
    value: str = Query(..., min_length=8, max_length=16, regex="^a"),
    values: List[str] = Query(default=["v1", "v2"], alias="alias_name")
):
    """多个查询参数的列表，参数别名"""
    return values


"""请求体和字段(Request Body and Fields)"""


class CityInfo(BaseModel):
    name: str = Field(..., example="Beijing", description="城市名称")
    country: str
    country_code: str = None
    country_population: int = Field(default=800, title="人口数量", description="国家人口数量")

    class Config:
        schema_extra = {
            "example": {
                "name": "Shanghai",
                "country": "China",
                "country_code": "CN",
                "country_population": 14e8,
            }
        }


@app03.post("/request_body/city")
async def city_info(city: CityInfo):
    print(city.name, city.country)
    return city.dict()


"""多参数混合(Request Body + Path Parameters + Query Parameters)"""


@app03.put("/request_body/city/{name}")
async def mix_city_info(
    name: str,
    city01: CityInfo,
    city02: CityInfo,
    confirmed: int = Query(ge=0, description="确诊数", default=0),
    death: int = Query(ge=0, description="死亡数", default=0)
):
    if name == "Shanghai":
        return {"Shanghai": {"confirmed": confirmed, "death": death}}

    return city01.dict(), city02.dict()


"""数据格式嵌套的请求体(Request Body - Nested Models)"""


class Data(BaseModel):
    city: List[CityInfo] = None
    date: date
    confirmed: int = Field(ge=0, description="确诊数", default=0)
    deaths: int = Field(ge=0, description="死亡数", default=0)
    recovered: int = Field(ge=0, description="痊愈数", default=0)


@app03.put("/request_body/nested")
async def nested_model(data: Data):
    return data


"""Cookie 和 Header 参数"""


@app03.get("/cookie")
async def cookie(cookie_id: Optional[str] = Cookie(None)):
    return {"cookie_id": cookie_id}


@app03.get("/header")
async def header(
    user_agent: Optional[str] = Header(None, convert_underscores=True),
    x_token: List[str] = Header(None)
):
    """有些HTTP代理和服务器是不允许在请求头中带有下划线的，所以 Header 提供了 convert_underscores 参数。
    convert_underscores 设置为 True 时，会将 user_agent 转换成 user-agent
    """
    return {"User-Agent": user_agent, "x_token": x_token}
