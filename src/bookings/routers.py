from typing import List

from fastapi import APIRouter, status

from src.bookings.schemas import BaseBookingType
from src.bookings.services import BookingTypeService


router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get(
    "/all_booking_types",
    status_code=status.HTTP_200_OK,
    response_model=List[BaseBookingType],
)
async def get_all_booking_types():
    all_booking_types = await BookingTypeService.get_all()
    return all_booking_types
