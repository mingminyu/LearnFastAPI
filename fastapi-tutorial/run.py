# coding: utf8
# ================================
# Author: yumingmin
# Cate: FastAPI
# Create Time: 2022/7/4 
# Update Time: 2022/7/4 18:35
# ================================
import time

import uvicorn
from requests import RequestException
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from fastapi.exceptions import RequestValidationError

from tutorial import app03, app04, app05, app06, app07, app08
from coronavirus import application


app = FastAPI(
    title="FastAPI Tutorial and Coronavirus Tracker API Docs",
    description="FastAPI 教程于新冠病毒追踪器示例，Github: http://github.com/liaogx/fastapi-tutorial",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redocs"
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1",
        "http://127.0.0.1:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(app03, prefix="/ch03", tags=["第三章 请求参数和验证"])
app.include_router(app04, prefix="/ch04", tags=["第四章 响应处理和FastAPI配置"])
app.include_router(app05, prefix="/ch05", tags=["第五章 FastAPI的依赖注入系统"])
app.include_router(app06, prefix="/ch06", tags=["第六章 安全、认证和授权"])
app.include_router(app07, prefix="/ch07", tags=["第七章 FastAPI的数据库操作和多应用的目录结构设计"])
app.include_router(app08, prefix="/ch08", tags=["第八章 中间件、CORS、后台任务、测试用例"])
app.include_router(application, prefix="/coronavirus", tags=["新冠病毒疫情跟踪器API"])

# 挂载静态文件目录，这个不会在 API 交互文档中显示
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")


# @app.exception_handler(StarletteHTTPException)
# async def http_exception_handler(request, exc):
#     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
#
#
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     return PlainTextResponse(str(exc), status_code=400)


if __name__ == '__main__':
    # 使用 uvicorn 运行服务: uvicorn run:app --reload
    uvicorn.run("run:app", host="127.0.0.1", port=8000, reload=True, debug=True, workers=4)
