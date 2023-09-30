from pydantic import Field, EmailStr

from src.base.schemas import BaseConfigSchema


class AuthUserLoginSchema(BaseConfigSchema):
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8)


class AuthUserRegistrationSchema(AuthUserLoginSchema):
    first_name: str = Field(..., max_length=100)
    telegram: str = Field(..., max_length=50)


class AuthUserRefreshSchema(BaseConfigSchema):
    refresh_token: str
