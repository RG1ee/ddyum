from pydantic import BaseModel, Field, EmailStr


class AuthUserRegistrationSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8)


class AuthUserSchema(AuthUserRegistrationSchema):
    pass


class AuthUserRefreshSchema(BaseModel):
    refresh_token: str
