import asyncio

import pytest
from httpx import AsyncClient
import json

from sqlalchemy import insert

from src.database.db import Base, engine, async_session
from src.main import app as fastapi_app
from src.config.settings import settings
from src.users.models import Profile, User
from src.bookings.models import BookingType


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"src/tests/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    users = open_mock_json("users")
    profile = open_mock_json("profile")
    booking_type = open_mock_json("booking_type")

    async with async_session() as session:
        add_users = insert(User).values(users)
        add_profile = insert(Profile).values(profile)
        add_booking_type = insert(BookingType).values(booking_type)

        await session.execute(add_users)
        await session.execute(add_profile)
        await session.execute(add_booking_type)

        await session.commit()


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def client():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="function")
async def authenticated_client():
    async with AsyncClient(app=fastapi_app, base_url="http://test.com") as client:
        data = {
            "email": "test@test.com",
            "password": "testpassword",
        }
        token_response = await client.post(
            f"{settings.API_PREFIX}/auth/token", json=data
        )

        assert token_response.status_code == 200

        access_token = token_response.json().get("access")
        client.headers = {"Authorization": f"Bearer {access_token}"}

        yield client


@pytest.fixture(scope="function")
async def admin_client():
    async with AsyncClient(app=fastapi_app, base_url="http://test.com") as client:
        data = {
            "email": "admin@test.com",
            "password": "testpassword",
        }
        token_response = await client.post(
            f"{settings.API_PREFIX}/auth/token", json=data
        )

        assert token_response.status_code == 200

        access_token = token_response.json().get("access")
        client.headers = {"Authorization": f"Bearer {access_token}"}

        yield client
