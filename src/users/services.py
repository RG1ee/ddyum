from sqlalchemy import update

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


class ProfileService(BaseService):
    model = Profile
