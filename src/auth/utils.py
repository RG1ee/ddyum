from datetime import datetime, timedelta
from typing import Any

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt

from src.config.settings import settings
from src.users.services import UserService
from src.exceptions.http_exceptions import http_exc_401_unauthorized


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")


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
        raise http_exc_401_unauthorized


async def authenticate_user(email: str, password: str):
    user = await UserService.get_one_or_none(email=email)
    if not user or not is_verify_password(password, user.hashed_password):
        return None
    return user


async def return_tokens(sub: dict):
    access_token = create_token(sub, settings.ACCESS_EXPIRE)
    refresh_token = create_token(sub, settings.REFRESH_EXPIRE)

    return dict(access=access_token, refresh=refresh_token, token_type="bearer")


async def check_token(payload: dict[str, Any]):
    expire: str | None = payload.get("exp")
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise http_exc_401_unauthorized

    user_id: str | None = payload.get("sub")
    if not user_id:
        raise http_exc_401_unauthorized

    user = await UserService.get_one_or_none(email=user_id)
    if not user:
        raise http_exc_401_unauthorized

    return user
