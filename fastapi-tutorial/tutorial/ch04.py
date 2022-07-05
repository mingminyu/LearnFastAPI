# coding: utf8
# ================================
# Author: yumingmin
# Cate: FastAPI
# Create Time: 2022/7/4 18:31:00
# Update Time:
# ================================
from fastapi import APIRouter, status, Form, File
from typing import Optional, List, Union
from pydantic import BaseModel, EmailStr

app04 = APIRouter()


"""响应模型(Response Model)"""


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    mobile: str = "10086"
    address: str = None
    full_name: Optional[str]


class UserOut(BaseModel):
    username: str
    email: EmailStr
    mobile: str = "10086"
    address: str = None
    full_name: Optional[str]


users = {
    "user01": {"username": "user01", "password": "123", "email": "user01@example.com"},
    "user02": {"username": "user02", "password": "456", "email": "user02@example.com", "mobile": "12345678910"}
}


@app04.post("/response_model", response_model=UserOut, response_model_exclude_unset=True)
async def response_model(user: UserIn):
    """
    - response_model 这样的参数操作称之为路径操作
    - response_model_exclude_unset 设置为 True 时，默认值不显示
    """
    print(user.password)
    return users["user02"]


@app04.post(
    "/response_model/attributes",
    response_model=Union[UserIn, UserOut],
    response_model_exclude=["username"],
    response_model_include=["username", "email"]
)
async def response_model_attributes(user: UserIn):
    """使用 Union[UserIn, UserOut] 后，删除 password 属性也能返回成功，如果希望删除 password 字段，则可以使用 del
    * 除此之外，还有 response_model_include=["username", "email"] 用来指定需要包含的字段，
    * response_model_exclude=["password"] 用来指定哪些字段不需要被包含
    * 如果 response_model_include 和 response_model_exclude 都包含了某个字段，则该字段不被包含
    """
    return user


"""响应状态码(Response Status Code)"""


@app04.post("/status_code", status_code=200)
async def status_code():
    return {"status_code": 200}


@app04.post("/status_attribute", status_code=status.HTTP_200_OK)
async def status_attribute():
    print(status.HTTP_200_OK)
    return {"status_code": status.HTTP_200_OK}


"""表单数据处理(Form Data)"""
@app04.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    """使用 Form 类需要安装 python-multipart
    Form 表单校验方法类似于 Body / Query / Cookie
    """
    return {"username": username}


"""单文件、多文件上传及参数详解(Request Files)"""


@app04.post("/file")
async def file_(file: bytes = File(...)):
    return {"file_size": len(file)}


