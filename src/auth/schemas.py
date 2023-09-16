from pydantic import Field, EmailStr

from src.base.schemas import BaseConfigSchema


class AuthUserRegistrationSchema(BaseConfigSchema):
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8)


class AuthUserSchema(AuthUserRegistrationSchema):
    pass


class AuthUserRefreshSchema(BaseConfigSchema):
    refresh_token: str
