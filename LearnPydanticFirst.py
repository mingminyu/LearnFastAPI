# coding: utf8
from datetime import datetime
from typing import List, Optional
from pathlib import Path
from pydantic import BaseModel, ValidationError

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


# 1. Pydantic 基础使用
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

# 2. 模型类的属性和方法
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
