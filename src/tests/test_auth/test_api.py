import pytest
from httpx import AsyncClient

from src.config.settings import settings


@pytest.mark.parametrize(
    "email, password, status_code, first_name, telegram",
    [
        ("test@email.com", "testpassword", 201, "Kolya", "kolya"),
        ("test@email.com", "testpassword1", 400, "Petya", "petya"),
    ],
)
async def test_register_user(
    email: str,
    password: str,
    first_name: str,
    telegram: str,
    status_code: int,
    client: AsyncClient,
):
    data = {
        "email": email,
        "password": password,
        "firstName": first_name,
        "telegram": telegram,
    }
    response = await client.post(
        f"{settings.API_PREFIX}/auth/register",
        json=data,
    )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("test@test.com", "testpassword", 200),
        ("test@test.com", "testpassword1", 400),
    ],
)
async def test_login_user(
    email: str,
    password: str,
    status_code: int,
    client: AsyncClient,
):
    response = await client.post(
        f"{settings.API_PREFIX}/auth/token",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == status_code
