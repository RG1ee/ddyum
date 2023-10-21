import pytest
from httpx import AsyncClient, Response

from src.config.settings import settings


async def test_get_all_booking_types(
    client: AsyncClient,
):
    response = await client.get(f"{settings.API_PREFIX}/bookings/booking-types")

    # check status code
    assert response.status_code == 200

    # checking for the number of booking types
    assert len(response.json()) == 2


async def test_get_all_booked_types(
    client: AsyncClient,
):
    response = await client.get(f"{settings.API_PREFIX}/bookings/booked-date")

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
        f"{settings.API_PREFIX}/bookings/",
        json=data,
    )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "name, description, status, is_authenticated, is_admin",
    [
        ("Couple", "Couple Test", 401, False, False),
        ("Couple", "Couple Test", 403, True, False),
        ("Couple", "Couple Test", 201, True, True),
    ],
)
async def test_create_booking_types_not_authenticated(
    client: AsyncClient,
    authenticated_client: AsyncClient,
    admin_client: AsyncClient,
    name: str,
    description: str,
    status: int,
    is_authenticated: bool,
    is_admin: bool,
):
    data = {
        "name": name,
        "description": description,
    }
    if not is_authenticated:
        response: Response = await client.post(
            f"{settings.API_PREFIX}/bookings/booking-types",
            json=data,
        )

    elif is_authenticated and not is_admin:
        response: Response = await authenticated_client.post(
            f"{settings.API_PREFIX}/bookings/booking-types",
            json=data,
        )

    else:
        response: Response = await admin_client.post(
            f"{settings.API_PREFIX}/bookings/booking-types",
            json=data,
        )

    assert response.status_code == status
