from pydantic import BaseModel, EmailStr


class UserBaseSchema(BaseModel):
    email: EmailStr
    telegram: str
    phone: str
    is_acive: bool
