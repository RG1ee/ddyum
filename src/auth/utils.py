from datetime import datetime, timedelta
from typing import Any

from fastapi import HTTPException, Response, status
from passlib.context import CryptContext
from jose import JWTError, jwt

from src.config.settings import settings
from src.users.services import UserService


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_hash_password(password: str) -> str:
    return pwd_context.hash(password)


def is_verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_token(data: dict, exp: int) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=exp)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        settings.ALGORITHM,
    )
    return encode_jwt


def decode_token(token: str) -> dict[str, Any]:
    try:
        decode_jwt = jwt.decode(
            token,
            settings.SECRET_KEY,
            settings.ALGORITHM,
        )
        return decode_jwt

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


async def authenticate_user(email: str, password: str):
    user = await UserService.get_one_or_none(email=email)
    if not user or not is_verify_password(password, user.hashed_password):
        return None
    return user


async def set_token(response: Response, sub: dict):
    access_token = create_token(sub, settings.ACCESS_EXPIRE)
    refresh_token = create_token(sub, settings.REFRESH_EXPIRE)

    response.set_cookie("access_token", access_token, httponly=True)
    response.set_cookie("refresh_token", refresh_token, httponly=True)


async def check_token(payload: dict[str, Any]):
    expire: str | None = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user_id: str | None = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user = await UserService.get_one_or_none(id=int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return user
