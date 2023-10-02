from src.bookings.services import BookingTypeService, BookingsService
from src.exceptions.http_exceptions import (
    http_exc_409_conflict,
    http_exc_404_booking_type_not_found,
)


async def check_existing_booking_and_booking_type(user_id: int, booking_id: int):
    existing_booking = await BookingsService.get_one_or_none(
        user_id=user_id,
        is_active=True,
    )
    if existing_booking:
        raise http_exc_409_conflict

    existing_booking_type = await BookingTypeService.get_one_or_none(id=booking_id)
    if not existing_booking_type:
        raise http_exc_404_booking_type_not_found
