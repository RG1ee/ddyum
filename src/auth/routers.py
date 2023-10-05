from fastapi import APIRouter, Depends, Response, status

from src.auth.schemas import (
    AuthUserLoginSchema,
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
from src.tasks.tasks import send_user_email
from src.users.models import User
from src.users.services import ProfileService, UserService
from src.exceptions.http_exceptions import (
    http_exc_400_bad_email,
    http_exc_400_bad_data,
    http_exc_401_unauthorized,
)
from src.base.email_utils import create_url_for_confirm


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    path="/register",
    status_code=status.HTTP_201_CREATED,
)
async def registration_user(payload: AuthUserRegistrationSchema) -> dict:
    existing_user = await UserService.get_one_or_none(email=payload.email)
    if existing_user:
        raise http_exc_400_bad_email
    hashed_password = create_hash_password(payload.password)
    new_user_id = await UserService.insert_data_returning_id(
        email=payload.email,
        hashed_password=hashed_password,
    )
    await ProfileService.insert_data(
        user_id=new_user_id,
        first_name=payload.first_name,
        telegram=payload.telegram,
    )

    send_user_email.delay(
        user_email=payload.email,
        template_name="email.html",
        url_for_confirm=create_url_for_confirm(payload.email),
    )

    return dict(email=payload.email)


@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
)
async def login_user(response: Response, payload: AuthUserLoginSchema):
    user = await authenticate_user(email=payload.email, password=payload.password)
    if not user:
        raise http_exc_400_bad_data

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
        raise http_exc_401_unauthorized

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
