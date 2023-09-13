from src.users.models import User

from src.services.base import BaseService


class UserService(BaseService):
    model = User
