from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.auth.schemas import (
    AuthUserSchema,
    AuthUserRegistrationSchema,
)
from src.auth.utils import (
    authenticate_user,
    check_token,
    decode_token,
    set_token,
    create_hash_password,
)
from src.auth.dependencies import current_user_for_refresh
from src.auth.tasks.tasks import send_user_verification_email
from src.users.models import User
from src.users.services import UserService


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
)
async def registration_user(payload: AuthUserRegistrationSchema) -> dict:
    existing_user = await UserService.get_one_or_none(email=payload.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    hashed_password = create_hash_password(payload.password)
    await UserService.insert_data(
        email=payload.email,
        hashed_password=hashed_password,
    )

    send_user_verification_email.delay(payload.email)

    return dict(email=payload.email)


@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
)
async def login_user(response: Response, payload: AuthUserSchema):
    user = await authenticate_user(email=payload.email, password=payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    await set_token(response, dict(sub=user.email))

    return dict(message="Successful login")


@router.get(
    path="/confirm/{access_token}",
    status_code=status.HTTP_200_OK,
)
async def confirm_user_email(access_token: str):
    sub = decode_token(access_token)
    user = await check_token(sub)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    await UserService.update_user(user_id=user.id, is_active=True)
    return user.email


@router.post(
    path="/refresh",
    status_code=status.HTTP_200_OK,
)
async def refresh(
    response: Response,
    current_user_for_refresh: User = Depends(current_user_for_refresh),
):
    await set_token(response, dict(sub=current_user_for_refresh.email))

    return dict(message="Successful refresh")


@router.get(
    path="/logout",
    status_code=status.HTTP_200_OK,
)
async def logout(response: Response) -> dict:
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return dict(message="Successful logout")
