from pathlib import Path
from typing import Literal
from functools import lru_cache

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    MODE: Literal["TEST", "DEV", "PROD"] = Field(default="DEV")
    POSTGRES_DSN: PostgresDsn = Field(
        default="postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/postgres",
    )
    TEST_DATABASE: str = Field(
        default=f"sqlite+aiosqlite:///db.sqlite3",
    )
    BROKER_URL: str = Field(default="redis://localhost:6379/0")
    ACCESS_EXPIRE: int = Field(default=10)
    REFRESH_EXPIRE: int = Field(default=10080)
    SECRET_KEY: str = Field(default="secret")
    ALGORITHM: str = Field(default="HS256")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
        env_file_encoding="utf-8",
    )


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
