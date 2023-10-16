from fastapi import APIRouter, status

from src.auth.schemas import (
    AuthUserLoginSchema,
    AuthUserRegistrationSchema,
    RefreshTokenSchema,
    TokensSchema,
)
from src.auth.utils import (
    authenticate_user,
    check_token,
    decode_token,
    return_tokens,
    create_hash_password,
)
from src.tasks.tasks import send_user_email
from src.users.services import ProfileService, UserService
from src.exceptions.http_exceptions import (
    http_exc_400_bad_email,
    http_exc_400_bad_data,
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
    path="/token",
    status_code=status.HTTP_200_OK,
    response_model=TokensSchema,
)
async def login_user(payload: AuthUserLoginSchema):
    user = await authenticate_user(email=payload.email, password=payload.password)

    if not user:
        raise http_exc_400_bad_data

    return await return_tokens(dict(sub=user.email))


@router.get(
    path="/confirm/{access_token}",
    status_code=status.HTTP_200_OK,
)
async def confirm_user_email(access_token: str):
    sub = decode_token(access_token)
    user = await check_token(sub)

    await UserService.update_user(user_id=user.id, is_active=True)
    return user.email


@router.post(
    path="/token/refresh",
    status_code=status.HTTP_200_OK,
    response_model=TokensSchema,
)
async def refresh(
    payload: RefreshTokenSchema,
):
    sub = decode_token(payload.refresh_token)
    user = await check_token(sub)

    return await return_tokens(dict(sub=user.email))
