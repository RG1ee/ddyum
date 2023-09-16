from pydantic import EmailStr

from src.base.schemas import BaseConfigSchema


class UserBaseSchema(BaseConfigSchema):
    email: EmailStr
    telegram: str
    phone: str
    is_acive: bool
