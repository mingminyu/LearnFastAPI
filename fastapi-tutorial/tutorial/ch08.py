# coding: utf8
# ================================
# Author: yumingmin
# Cate: FastAPI
# Create Time: 2022/7/4 18:31:00
# Update Time:
# ================================

import time
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends

app08 = APIRouter()

"""中间件(Middleware)
* 带 `yield` 的依赖的退出部分的代码和后台任务会在中间件之后运行
"""

"""跨资源共享(Cross-Origin Resource Sharing, CORS)"""

"""后台任务(Background Tasks)"""


def bg_task(framework: str):
    time.sleep(5)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("bg_test.txt", mode="a") as f:
        f.write(f"{now}: add this message of {framework}!\n")


@app08.post("/background_tasks")
async def run_bg_task(framework: str, background_task: BackgroundTasks):
    """实现后台任务
    :param framework: 被调用的后台函数的参数
    :param background_task: FastAPI.BackgroundTasks
    :return:
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    background_task.add_task(bg_task, framework)
    return {"message": f"{now}: 任务已经在后台运行"}


def continue_write_readme(background_tasks: BackgroundTasks, q: Optional[str] = None):
    if q:
        background_tasks.add_task(bg_task, "\n> 整体的介绍 FastAPI，快速上手开发，结合 API 交互文档逐个讲解核心模块的使用")
    return q


@app08.post("/dependency/background_tasks")
async def dependency_run_bg_task(q: str = Depends(continue_write_readme)):
    if q:
        return {"message": "bg_test.txt 更新成功"}
