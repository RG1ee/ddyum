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
