# coding: utf8
# ================================
# Author: yumingmin
# Cate: FastAPI
# Create Time: 2022/7/4 18:31:00
# Update Time:
# ================================

"""Relational SQL Database FastAPI 数据库操作
多应用的目录结构设计(Bigger Applications, Multiple Files)
"""

from fastapi import APIRouter, Request, Depends


async def get_user_agent(request: Request):
    print(request.headers["User-Agent"])

app07 = APIRouter(
    prefix="/bigger_applications",
    tags=["第七章 FastAPI的数据库操作和多应用的目录结构设计"],
    dependencies=[Depends(get_user_agent)],
    responses={200: {"description": "Good job!"}},
)


@app07.get("/bigger_applications")
async def bigger_applications():
    return {"message": "Bigger Applications - Multiple Files"}
