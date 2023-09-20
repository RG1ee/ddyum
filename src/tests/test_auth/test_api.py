import pytest
from httpx import AsyncClient

from src.users.services import UserService
from src.config.settings import settings


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("test@email.com", "testpassword", 201),
        ("test@email.com", "testpassword1", 400),
    ],
)
async def test_register_user(
    email: str,
    password: str,
    status_code: int,
    client: AsyncClient,
):
    response = await client.post(
        f"{settings.API_PREFIX}/auth/register",
        json={"email": email, "password": password},
    )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email, password, status_code, token",
    [
        ("test@test.com", "testpassword", 200, True),
        ("test@test.com", "testpassword1", 400, False),
    ],
)
async def test_login_user(
    email: str,
    password: str,
    status_code: int,
    client: AsyncClient,
    token: bool,
):
    response = await client.post(
        f"{settings.API_PREFIX}/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == status_code

    assert ("access_token" in client.cookies) is token
    assert ("refresh_token" in client.cookies) is token


async def test_confirm_email(
    not_active_client: AsyncClient,
):
    response = await not_active_client.get(
        f"{settings.API_PREFIX}/auth/confirm/{not_active_client.cookies['access_token']}",
    )

    assert response.status_code == 200

    user = await UserService.get_one_or_none(email=response.json())
    assert user.is_active is True


async def test_logout_user(authenticated_client: AsyncClient):
    response = await authenticated_client.get(f"{settings.API_PREFIX}/auth/logout")

    assert response.status_code == 200

    assert "access_token" not in response.cookies
