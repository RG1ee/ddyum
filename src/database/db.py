from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine

from src.config.settings import settings


if settings.MODE == "TEST":
    DATABASE_URL = settings.TEST_DATABASE
    # DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = str(settings.POSTGRES_DSN)

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    ...
