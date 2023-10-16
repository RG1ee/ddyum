from fastapi import Depends

from src.auth.utils import check_token, decode_token, oauth2_scheme


async def current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    return await check_token(payload)
