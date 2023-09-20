from fastapi import Depends, HTTPException, Request, status

from src.auth.utils import check_token, decode_token
from src.exceptions.http_exceptions import http_exc_401_unauthorized


def get_token(request: Request):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    if not access_token or not refresh_token:
        raise http_exc_401_unauthorized
    return access_token, refresh_token


async def current_user(token: tuple = Depends(get_token)):
    payload = decode_token(token[0])
    return await check_token(payload)


async def current_user_for_refresh(token: tuple = Depends(get_token)):
    payload = decode_token(token[1])
    return await check_token(payload)
