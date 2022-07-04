# coding: utf8
# ================================
# Author: yumingmin
# Cate: 
# Create Time: 2022/7/4 
# Update Time: 2022/7/4 18:35
# ================================
import uvicorn
from fastapi import FastAPI
from tutorial import app03, app04, app05


app = FastAPI()
app.include_router(app03, prefix="/ch03", tags=["第三章 请求参数和验证"])
app.include_router(app04, prefix="/ch04", tags=["第四章 响应处理和FastAPI配置"])
app.include_router(app05, prefix="/ch05", tags=["第五章 FastAPI的依赖注入系统"])


if __name__ == '__main__':
    # 使用 uvicorn 运行服务: uvicorn run:app --reload
    uvicorn.run("run:app", host="127.0.0.1", port=8000, reload=True, debug=True, workers=1)
