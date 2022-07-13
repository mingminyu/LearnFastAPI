# coding: utf8
# ================================
# Author: yumingmin
# Cate: FastAPI
# Create Time: 2022/7/4 18:31:00
# Update Time:
# ================================

"""OAuth2.0 授权模式
* 授权码授权模式(Authorization Code Grant)
* 隐式授权模式(Implicit Grant)
* 密码授权模式(Resource Owner Password Credentials Grant)
* 客户端凭证授权模式（Client Credentials Grant）
"""
from datetime import date, datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import JWTError, jwt

app06 = APIRouter()


"""OAuth2 密码模式和 FastAPI 的 OAuth2PasswordBearer
* OAuth2PasswordBearer 是接收 URL 作为参数的一个类，客户端会向该 URL 发送 username 和 password 参数
* OAuth2PasswordBearer 并不会创建相应的 URL 路径操作，只是指明客户端用来请求 Token 的 URL 地址
* 当请求到来的时候，FastAPI 会检查请求的 Authorization Header信息，如果没有找到 Authorization Header信息，
"""

# 请求 Token 的 URL 地址：https://127.0.0.1:8000/ch06/token
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/ch06/token")


@app06.get("/oauth2_password_bearer")
async def oauth2_password_bearer(token: str = Depends(oauth2_schema)):
    return {"token": token}


"""基于 Password 和 Bearer token 的 OAuth2 认证"""
fake_users_db = {
    "jay": {
        "username": "jay",
        "email": "jay@example.com",
        "hashed_password": "fakehashedabc",
        "disabled": False
    },
    "jj": {
        "username": "jj",
        "email": "jj@example.com",
        "hashed_password": "fakehashedefg",
        "disabled": True
    },
}

def fake_hash_password(password: str):
    return "fakehashed" + password


class User(BaseModel):
    username: str
    email: EmailStr
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token: str):
    user = get_user(fake_users_db, token)
    return user


def get_current_user(token: str = Depends(oauth2_schema)):
    """`headers={"WWW-Authenticate": "Bearer"}` 为 OAuth2 的规范，
    请求失败时返回
    """
    user = fake_decode_token(token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid authorization credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    return current_user


@app06.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)

    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username"
        )

    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)

    if hashed_password != user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )

    return {"access_token": user.username, "token_type": "bearer"}


@app06.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


"""开发基于JSON Web Token(OAuth2 with password and hashing, Bearer with JWT Token)"""

SECRET_KEY = "abc123456"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class UserToken(BaseModel):
    """返回给用户的 token"""
    access_token: str
    token_type: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/ch06/jwt/token")

# 之前的数据中 hashed_password 并未经过 Hash 加密，所以选择 jay / jj 会导致 Internal Error
fake_users_db.update({
    "john snow": {
        "username": "john snow",
        "email": "johnsnow@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
})


def verify_password(plain_password, hashed_password):
    """对密码进行校验"""
    print(plain_password, hashed_password)
    return pwd_context.verify(plain_password, hashed_password)


def jwt_get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def jwt_authenticate_user(db, username: str, password: str):
    user = jwt_get_user(db, username)

    if not user:
        return False

    if not verify_password(plain_password=password, hashed_password=user.hashed_password):
        return False

    return user


def created_access_token(data: dict, expire_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


@app06.post("/jwt/token", response_model=UserToken)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = jwt_authenticate_user(
        db=fake_users_db,
        username=form_data.username,
        password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = created_access_token(
        data={"sub": user.username},
        expire_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


async def jwt_get_current_user(token: str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = jwt_get_user(db=fake_users_db, username=username)

    if user is None:
        raise credentials_exception

    return user


async def jwt_get_current_active_user(current_user: User = Depends(jwt_get_current_user)):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    return current_user


@app06.post("/jwt/users/me")
async def read_users_me(current_user: User = Depends(jwt_get_current_active_user)):
    return current_user
