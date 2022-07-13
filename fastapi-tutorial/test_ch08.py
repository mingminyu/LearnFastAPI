# coding: utf8
# ===================================
# Author: yumingmin
# File: test_ch08.py
# Cate: FastAPI
# Create time: 2022/7/9 23:15
# Update time: 
# ===================================

from fastapi.testclient import TestClient

from run import app

"""Testing 测试用例
* 函数名用 test_ 开头是 pytest 的规范。注意不是 async def
"""

client = TestClient(app)


def test_run_bg_task():
    response = client.post(url="/ch08/background_tasks?framework=FastAPI")
    assert response.status_code == 200
    assert response.json() != {"message": "任务已在后台运行"}


def test_dependency_run_bg_task():
    response = client.post(url="/ch08/dependency/background_tasks")
    assert response.status_code == 200
    assert response.json() is None


def test_dependency_run_bg_task_q():
    response = client.post(url="/ch08/dependency/background_tasks?q=1")
    assert response.status_code == 200
    assert response.json() == {"message": "bg_test.txt 更新成功"}
