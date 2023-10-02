from src.base.services import BaseService

from src.bookings.models import BookingType, Bookings


class BookingTypeService(BaseService):
    model = BookingType


class BookingsService(BaseService):
    model = Bookings
