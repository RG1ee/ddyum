from httpx import AsyncClient
import pytest

from src.config.settings import settings


@pytest.mark.parametrize(
    "user_id, email, first_name, telegram, status",
    [
        (1, "test@test.com", "John", "john", 200),
    ],
)
async def test_get_user_profile(
    client: AsyncClient,
    authenticated_client: AsyncClient,
    user_id: int,
    first_name: str,
    email: str,
    telegram: str,
    status: int,
):
    response = await authenticated_client.get(f"{settings.API_PREFIX}/users/my_profile")

    assert response.json() == {
        "id": user_id,
        "email": email,
        "firstName": first_name,
        "telegram": telegram,
    }
    assert response.status_code == status

    response = await client.get(f"{settings.API_PREFIX}/users/my_profile")
    assert response.status_code == 401


@pytest.mark.parametrize(
    "first_name, telegram, status_code",
    [
        ("Monika", "monika123", 200),
    ],
)
async def test_update_profile(
    authenticated_client: AsyncClient,
    client: AsyncClient,
    first_name,
    telegram,
    status_code,
):
    data = {
        "firstName": first_name,
        "telegram": telegram,
    }

    # test patch update user profile
    response = await authenticated_client.patch(
        f"{settings.API_PREFIX}/users/my_profile/update", json=data
    )

    assert response.status_code == status_code
    assert response.json() == data

    # test of an un-authenticated user
    response = await client.patch(
        f"{settings.API_PREFIX}/users/my_profile/update", json=data
    )

    assert response.status_code == 401
