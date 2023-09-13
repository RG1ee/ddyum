from pydantic import BaseModel, EmailStr, Field


class UserBaseSchema(BaseModel):
    email: EmailStr
    telegram: str
    phone: str
    is_acive: bool


class UserRegistrationSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
