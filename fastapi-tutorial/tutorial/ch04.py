# coding: utf8
# ================================
# Author: yumingmin
# Cate: FastAPI
# Create Time: 2022/7/4 18:31:00
# Update Time:
# ================================
from fastapi import APIRouter, status, Form, File, UploadFile, HTTPException
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
async def fileupload(file: bytes = File(...)):
    """bytes 的方式只适合上传小文件
    如果要上传多个文件，可以使用 file: List[bytes] = File(...)
    """
    return {"file_size": len(file)}


@app04.post("/upload_files")
async def upload_files(files: List[UploadFile] = File(...)):
    """
    使用 UploadFile 类的优势：

    1. 文件存储在内存中，使用的内存达到阈值后，蒋被保存在磁盘中
    2. 适合图片、视频大文件
    3. 可以获取上传文件的元数据，如文件名、创建时间等
    4. 有文件对象的异步接口
    5. 上传的文件是 Python 文件对象，可以使用 write、seek 等方法
    """
    for file in files:
        contents = await file.read()
        print(len(contents))

    return {"filename": files[0].filename, "content_type": files[0].content_type}


"""静态文件配置(Static Files)"""

"""路径操作配置(Path Operation Configuration)"""


@app04.post(
    "/path_operation_configuration",
    response_model=UserOut,
    tags=["Path", "Operation", "Configuration"],
    summary="This is a summary",
    description="This is a description",
    response_description="This is a response description",
    status_code=status.HTTP_200_OK,
    deprecated=True
)
async def path_operation_configuration(user: UserIn):
    return user.dict()


"""应用常见配置项"""

"""错误处理(Handing Errors)"""


@app04.get("/http_exception")
async def http_exception(city: str):
    if city != "Beijing":
        raise HTTPException(status_code=404, detail="City Not Found!", headers={'X-Error': 'error'})

    return {"city": city}


@app04.get("/http_exception/{city_id}")
async def override_http_exception(city_id: int):
    if city_id == 1:
        raise HTTPException(status_code=418, detail="Nope! I don't like")

    return {"city_id": city_id}
