from httpx import AsyncClient
import pytest

from src.config.settings import settings


@pytest.mark.parametrize(
    "user_id, email, first_name, telegram, phone, status",
    [
        (1, "test@test.com", "John", "john", "89321231212", 200),
    ],
)
async def test_get_user_profile(
    client: AsyncClient,
    authenticated_client: AsyncClient,
    user_id: int,
    first_name: str,
    email: str,
    telegram: str,
    phone: str,
    status: int,
):
    response = await authenticated_client.get(f"{settings.API_PREFIX}/users/my_profile")

    assert response.json() == {
        "id": user_id,
        "email": email,
        "firstName": first_name,
        "telegram": telegram,
        "phone": phone,
    }
    assert response.status_code == status

    response = await client.get(f"{settings.API_PREFIX}/users/my_profile")
    assert response.status_code == 401


@pytest.mark.parametrize(
    "first_name, telegram, phone",
    [
        ("Monika", "monika123", "8932121155"),
    ],
)
async def test_update_profile(
    authenticated_client: AsyncClient,
    client: AsyncClient,
    first_name: str,
    telegram: str,
    phone: str,
):
    data = {
        "firstName": first_name,
        "telegram": telegram,
        "phone": phone,
    }

    # test patch update user profile
    response = await authenticated_client.patch(
        f"{settings.API_PREFIX}/users/my_profile/update", json=data
    )

    assert response.status_code == 200
    assert response.json() == data

    # test of an un-authenticated user
    response = await client.patch(
        f"{settings.API_PREFIX}/users/my_profile/update", json=data
    )

    assert response.status_code == 401

    # test partial update
    data.pop("phone")
    response = await authenticated_client.patch(
        f"{settings.API_PREFIX}/users/my_profile/update", json=data
    )

    assert response.status_code == 200
    assert response.json() == data
