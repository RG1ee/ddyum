from src.base.services import BaseService

from src.bookings.models import BookingType


class BookingTypeService(BaseService):
    model = BookingType
