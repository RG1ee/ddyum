from sqlalchemy import insert, select
from src.database.db import async_session


class BaseService:
    model = None

    @classmethod
    async def get_one_or_none(cls, **filters):
        async with async_session() as session:
            query = select(cls.model.__table__.columns).filter_by(**filters)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def insert_data(cls, **data):
        async with async_session() as session:
            stmt = insert(cls.model).values(**data)
            await session.execute(stmt)
            await session.commit()
