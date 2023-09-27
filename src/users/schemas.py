from pydantic import EmailStr

from src.base.schemas import BaseConfigSchema


class UserBaseSchema(BaseConfigSchema):
    id: int
    email: EmailStr
    telegram: str | None
    phone: str | None


class ProfileSchema(BaseConfigSchema):
    id: int
    email: EmailStr
    first_name: str | None
    telegram: str | None
    phone: str | None
