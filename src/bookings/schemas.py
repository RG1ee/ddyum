from datetime import date

from pydantic import Field
from src.base.schemas import BaseConfigSchema


class BaseBookingType(BaseConfigSchema):
    id: int
    name: str
    description: str | None = None


class CreateBookingSchema(BaseConfigSchema):
    booking_id: int = Field(...)
    booking_date: date = Field(...)
