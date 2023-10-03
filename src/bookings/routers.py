from typing import List

from fastapi import APIRouter, Depends, status

from src.auth.dependencies import current_user
from src.bookings.schemas import BaseBookingType, CreateBookingSchema
from src.bookings.services import BookingTypeService, BookingsService
from src.users.models import User
from src.bookings.utils import check_existing_booking_and_booking_type, cache


router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get(
    "/all_booking_types",
    status_code=status.HTTP_200_OK,
    response_model=List[BaseBookingType],
)
@cache(expire=60 * 60)
async def get_all_booking_types():
    all_booking_types = await BookingTypeService.get_all()
    return all_booking_types


@router.get(
    "/booked_date",
    status_code=status.HTTP_200_OK,
)
async def get_booked_date():
    all_booked_date = await BookingsService.get_all_booked_date(is_active=True)
    return all_booked_date


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
)
async def create_booking(
    payload: CreateBookingSchema,
    current_user: User = Depends(current_user),
):
    await check_existing_booking_and_booking_type(current_user.id, payload.booking_id)

    await BookingsService.insert_data(
        user_id=current_user.id,
        booking_type=payload.booking_id,
        booking_date=payload.booking_date,
    )

    # TODO send email

    return dict(message="Successful")
