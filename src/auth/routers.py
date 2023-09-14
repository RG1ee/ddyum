from fastapi import APIRouter, HTTPException, Response, status

from src.auth.schemas import (
    AuthUserRefreshSchema,
    AuthUserSchema,
    AuthUserRegistrationSchema,
)
from src.auth.utils import (
    authenticate_user,
    decode_token,
    set_token,
    create_hash_password,
)
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

    return dict(email=payload.email)


@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
)
async def login_user(response: Response, payload: AuthUserSchema):
    user = await authenticate_user(email=payload.email, password=payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    set_token(response, dict(sub=str(user.id)))

    return dict(message="Successful login")


@router.post(
    path="/refresh",
    status_code=status.HTTP_200_OK,
)
async def refresh(response: Response, payload: AuthUserRefreshSchema):
    user = await UserService.get_one_or_none(id=decode_token(payload.refresh_token))
    if not user:
        response.delete_cookie("refresh_token")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    set_token(response, dict(sub=str(user.id)))

    return dict(message="Successful refresh")


@router.post(
    path="/logout",
    status_code=status.HTTP_200_OK,
)
async def logout(response: Response) -> dict:
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return dict(message="Successful logout")
