# coding: utf8
# ================================
# Author: yumingmin
# Cate: FastAPI
# Create Time: 2022/7/4 18:31:00
# Update Time:
# ================================

"""FastAPI 的依赖注入系统
🔔 依赖注入
* `依赖注入`是指在编程中，为保证代码成功运行，先导入或声明所需要的`依赖`，如子函数、数据库连接等
* 提高代码复用率
* 共享数据库的连接
* 增强安全、认证和角色管理

🔔 兼容性
* 所有的关系型数据库，支持 NoSQL 数据库
* 第三方库和 API
* 认证和授权系统
* 秀响应数据注入系统
"""
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException

app05 = APIRouter()

"""创建、导入和声明依赖(Dependencies)"""


async def common_parameters(
    q: Optional[str] = None,
    page: int = 1,
    limit: int = 10
):
    return {"q": q, "page": page,  "limit": limit}


@app05.get("/dependency01")
async def dependency01(commons: dict = Depends(common_parameters)):
    return commons


@app05.get("/dependency02")
def dependency02(commons: dict = Depends(common_parameters)):
    return commons


"""类作为依赖(Classes as Dependencies)"""


fake_items_db = [
    {"item": "foo"},
    {"item": "bar"},
    {"item": "baz"},
]


class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, page: int = 1, limit: int = 10):
        self.q = q
        self.page = page
        self.limit = limit


@app05.get("/classes_as_dependencies01")
async def classes_as_dependencies(commons: CommonQueryParams = Depends(CommonQueryParams)):
    return commons


@app05.get("/classes_as_dependencies02")
async def classes_as_dependencies(commons: CommonQueryParams = Depends()):
    return commons


@app05.get("/classes_as_dependencies")
async def classes_as_dependencies(commons=Depends(CommonQueryParams)):
    response = {}
    if commons.q:
        response.update({"q": commons.q})

    items = fake_items_db[commons.page: commons.page + commons.limit]
    response.update({"item": items})
    return response


"""子依赖(Sub-dependencies)"""


def query(q: Optional[str] = None):
    return q


def sub_query(q: str = Depends(query), last_query: Optional[str] = None):
    if not q:
        return last_query

    return q


@app05.get("/sub_dependency")
async def sub_dependency(final_query: str = Depends(sub_query, use_cache=True)):
    """use_cache 默认为 True， 表示当多个依赖有一个共同的子依赖时，
    每次 request 请求指挥调用子依赖一次。"""
    return {"sub_dependency": final_query}


"""路径操作装饰器中的多依赖(Dependencies in Path Operation Decorators)"""


async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

    return x_token


async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")

    return x_key


@app05.get("/dependency_in_path_operation", dependencies=[Depends(verify_token), Depends(verify_key)])
async def dependency_in_path_operation():
    return [{"user": "user01"}, {"user": "user02"}]


"""全局依赖(Global Dependencies)"""

# 在 APIRouter() 中 `dependencies` 参数设置全局依赖
# 当然也可以在 FastAPI() 中设置 `dependencies` 参数，效果是一样的
app05 = APIRouter(dependencies=[Depends(verify_token), Depends(verify_key)])


"""带 yield 的依赖(Dependencies with yield)
需要 Python >= 3.7，如果是 Python==3.6，则需要安装 async-exit-stack async-generator
"""

