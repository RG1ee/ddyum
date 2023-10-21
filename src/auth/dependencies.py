from fastapi import Depends

from src.auth.utils import check_token, decode_token, oauth2_scheme
from src.users.models import User
from src.exceptions.http_exceptions import http_exc_403_forbidden


async def current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    return await check_token(payload)


async def current_admin_user(current_user: User = Depends(current_user)) -> User:
    if not current_user.is_admin:
        raise http_exc_403_forbidden

    return current_user
