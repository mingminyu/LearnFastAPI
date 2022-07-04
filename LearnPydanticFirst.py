# coding: utf8
from datetime import datetime, date
from typing import List, Optional
from pathlib import Path
from pydantic import BaseModel, ValidationError, constr
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base

"""
Pydantic使用
- 使用 Python 的类型注解来进行数据校验和 settings 管理
- Pydantic 可以在代码运行时提供类型提示，数据校验失败时提供友好地错误提示
- 定义数据应该如何在纯规范的 Python 代码种保存，并用 Pydantic 验证它
- PyCharm 可以安装 Pydantic 插件
"""


class User(BaseModel):
    id: int
    name: str = "Echo"
    signup_ts: Optional[datetime] = None,
    friends: List[int] = []


# ================== 1. Pydantic 基础使用 ==================
print("\033[31;31m =============1. Pydantic基础使用============= \033[0m")
external_data = {
    "id": 123,
    "signup_ts": "2022-06-28 21:29",
    "friends": [1, 2, "3"],  # 这里即使传入字符串 "3" 也可以被成功解析
}
user = User(**external_data)
print("ID of the user: ", user.id)
print("Name of the user: ", user.name)
print("Signup time of the user: ", user.signup_ts)
print("Friends of the user: ", user.friends)
print("Info of user: ", user.dict())

# 2. 校验失败处理
print("\033[31;31m =============2. 校验失败处理============= \033[0m")
try:
    User(id=1, signup_ts=datetime.today(), friends=[1, 2, "not number"])
except ValidationError as e:
    print(e.json())

# ================== 2. 模型类的属性和方法 ==================
print("\033[31;31m =============3. 模型类的属性和方法============= \033[0m")
print("Dict of user: ", user.dict())
print("Json of user: ", user.json())
print("Copy method of user: ", user.copy())  # 浅拷贝
print("`parse_obj` method: ", User.parse_obj(obj=external_data))
print("`parse_raw` method: ", User.parse_raw('{"id": 1, "signup_ts": "2022-06-28 21:29", "friends": [1, 2]}'))

# 也可以使用 parse_file 方法读取文件
path = Path("pydantic-tutorial.json")
path.write_text('{"id": 1, "signup_ts": "2022-06-28 21:29", "friends": [1, 2]}')
print("`parse_file` method: ", User.parse_file(path))
print("Schema of user", user.schema())
print("Schema JSON of user", user.schema_json())

# 如果不希望对数据进行验证，直接创建模型类，可以使用 `construct` 方法，这个方法并不常用
# 并不会因为传入数据并不符合参数设置而报错
user_data = {"id": "error", "signup_ts": "2022-06-28 21:29", "friends": [1, 2]}
print("`construct` method: ", User.construct(**user_data))

# 定义模型类的时候，所有字段都注明类型，字段顺序就不会乱
print(User.__fields__.keys())

# ================== 3. 递归模型 ==================
# 两个都继承了 BaseModel 的类，可以互相之间嵌套使用
print("\033[31;31m =============3. 递归模型============= \033[0m")


class Sound(BaseModel):
    sound: str


class Dog(BaseModel):
    birth: date
    weight: Optional[float] = None
    sound: List[Sound]


# {"sound": "wang wang"} 中 sound 对应 Sound 类
dogs = Dog(birth=date.today(), weight=6.66, sound=[{"sound": "wang wang"}, {"sound": "ying ying"}])
print(dogs.dict())

# ================== 4. ORM模型: 从类实例创建符合 ORM 对象的模型 ==================
print("\033[31;31m =============4. ORM模型: 从类实例创建符合 ORM 对象的模型============= \033[0m")

Base = declarative_base()


class CompanyORM(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, nullable=False)
    public_key = Column(String(20), index=True, nullable=False, unique=True)
    name = Column(String(63), unique=True)
    domains = Column(ARRAY(String(255)))


class CompanyModel(BaseModel):
    id: int
    public_key: constr(max_length=20)
    name: constr(max_length=63)
    domains: List[constr(max_length=255)]

    class Config:
        orm_mode = True


co_orm = CompanyORM(
    id=123,
    public_key="foobar",
    name="test_orm",
    domains=["example.com", "imooc.com"]
)
print(CompanyModel.from_orm(co_orm))

# ================== 5. Pydantic支持的所有字段类型 ==================
# Doc URL: https://pydantic-docs.helpmanual.io/usage/types/
# 非常有必要进一步学习 Pydantic 的完整教程
print("\033[31;31m =============5. Pydantic支持的所有字段类型============= \033[0m")
print("你可以参考 Pydantic 官网文档: https://pydantic-docs.helpmanual.io/usage/types/")