from pydantic import BaseModel, Field, EmailStr

from src.base.schemas import BaseConfigSchema


class AccessTokenSchema(BaseModel):
    access_token: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class TokensSchema(BaseConfigSchema):
    access: str
    refresh: str
    token_type: str


class AuthUserLoginSchema(BaseConfigSchema):
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8)


class AuthUserRegistrationSchema(AuthUserLoginSchema):
    first_name: str = Field(..., max_length=100)
    telegram: str = Field(..., max_length=50)
