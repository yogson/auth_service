import abc
from typing import Optional

from models.user import UserInDB


class AbstractUsersDAO(abc.ABC):
    @abc.abstractmethod
    def get_user_by_name(self, username: str) -> Optional[UserInDB]:
        pass

    @abc.abstractmethod
    def save_user(self, user: UserInDB):
        pass
