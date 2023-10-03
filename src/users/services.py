from sqlalchemy import select, update

from src.users.models import Profile, User
from src.base.services import BaseService
from src.database.db import async_session


class UserService(BaseService):
    model = User

    @classmethod
    async def update_user(cls, user_id, **data):
        async with async_session() as session:
            stmt = update(cls.model).filter_by(id=user_id).values(**data)
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def get_user_with_profile(cls, user_id: int):
        async with async_session() as session:
            query = (
                select(
                    cls.model.email,
                    Profile.id,
                    Profile.first_name,
                    Profile.telegram,
                )
                .join(
                    Profile,
                    cls.model.id == Profile.user_id,
                )
                .filter_by(id=user_id)
            )
            result = await session.execute(query)
            return result.mappings().first()


class ProfileService(BaseService):
    model = Profile

    @classmethod
    async def update_data(cls, id: int, **data):
        async with async_session() as session:
            stmt = (
                update(cls.model)
                .returning(cls.model.__table__.columns)
                .filter_by(user_id=id)
                .values(**data)
            )
            result = await session.execute(stmt)
            await session.commit()

            return result.mappings().first()
