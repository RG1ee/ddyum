from src.base.schemas import BaseConfigSchema


class BaseBookingType(BaseConfigSchema):
    id: int
    name: str
    description: str | None = None
