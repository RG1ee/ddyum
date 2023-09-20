from pathlib import Path
from typing import Literal
from functools import lru_cache

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    MODE: Literal["TEST", "DEV", "PROD"] = Field(default="DEV")
    API_PREFIX: str = Field(default="/api/v1")
    POSTGRES_DSN: PostgresDsn = Field(
        default="postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/postgres",
    )
    TEST_DATABASE: str = Field(
        default=f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3",
    )
    BROKER_URL: str = Field(default="redis://localhost:6379/0")
    ACCESS_EXPIRE: int = Field(default=10)
    REFRESH_EXPIRE: int = Field(default=10080)
    EMAIL_TOKEN_EXPIRE: int = Field(default=120)
    SECRET_KEY: str = Field(default="secret")
    ALGORITHM: str = Field(default="HS256")
    BASE_URL: str = Field(default="http://127.0.0.1:8000/")

    # Smtp server
    SMTP_SERVER: str = Field(default="smtp.example.com")
    SMTP_PORT: int = Field(default=465)
    SMTP_LOGIN: str = Field(default="example@example.com")
    SMTP_PASSWORD: str = Field(default="example")

    # Email
    SUBJECT: str = Field(default="Your Subject")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
        env_file_encoding="utf-8",
    )


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
