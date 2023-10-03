from sqlalchemy import select
from src.base.services import BaseService

from src.bookings.models import BookingType, Bookings
from src.database.db import async_session


class BookingTypeService(BaseService):
    model = BookingType


class BookingsService(BaseService):
    model = Bookings

    @classmethod
    async def get_all_booked_date(cls, is_active):
        async with async_session() as session:
            query = select(cls.model.booking_date).where(
                cls.model.is_active == is_active
            )
            result = await session.execute(query)
            return result.mappings().all()
