import pytest
from httpx import AsyncClient

from src.config.settings import settings


async def test_get_all_booking_types(
    client: AsyncClient,
):
    response = await client.get(f"{settings.API_PREFIX}/bookings/all_booking_types")

    # check status code
    assert response.status_code == 200

    # checking for the number of booking types
    assert len(response.json()) == 2


async def test_get_all_booked_types(
    client: AsyncClient,
):
    response = await client.get(f"{settings.API_PREFIX}/bookings/booked_date")

    assert response.status_code == 200


@pytest.mark.parametrize(
    "booking_id, booking_date, status_code",
    [
        (3, "2023-10-02", 404),
        (1, "2023-10-02", 201),
        (2, "2023-10-07", 409),
    ],
)
async def test_create_booking(
    authenticated_client: AsyncClient,
    booking_id: int,
    booking_date: str,
    status_code: int,
):
    data = {
        "bookingId": booking_id,
        "bookingDate": booking_date,
    }
    response = await authenticated_client.post(
        f"{settings.API_PREFIX}/bookings/create",
        json=data,
    )

    assert response.status_code == status_code
