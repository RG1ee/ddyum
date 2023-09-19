import asyncio

import pytest
from httpx import AsyncClient
import json

from sqlalchemy import insert

from src.database.db import Base, engine, async_session
from src.main import app as fastapi_app
from src.config.settings import settings
from src.users.models import User


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

    async with async_session() as session:
        add_users = insert(User).values(users)

        await session.execute(add_users)
        await session.commit()


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def client():
    async with AsyncClient(app=fastapi_app, base_url="http://") as client:
        yield client


@pytest.fixture(scope="session")
async def authenticated_client():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as client:
        data = {
            "email": "test@test.com",
            "password": "testpassword",
        }
        await client.post("auth/login", json=data)

        assert client.cookies["access_token"]
        assert client.cookies["refresh_token"]

        yield client


@pytest.fixture(scope="function")
async def not_active_client():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as client:
        data = {
            "email": "testuser@test.com",
            "password": "testpassword",
        }
        await client.post("auth/login", json=data)

        assert client.cookies["access_token"]
        assert client.cookies["refresh_token"]

        yield client
