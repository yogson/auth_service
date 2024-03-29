from functools import cached_property
from pathlib import Path
from typing import Optional
from uuid import uuid4

from passlib.context import CryptContext

from api import exceptions
from api.settings import USERS_STORE
from dao.infile_user_dao import FileUsersDAO
from models.user import UserInDB, UserModel


class UserNotExist(Exception):
    pass


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


class LocalUser:
    users_db = FileUsersDAO(data_path=Path(USERS_STORE))

    def __init__(self, *, username: str = None, guid: str = None):
        self.username = username
        self.guid = guid

    @cached_property
    def _user(self) -> UserInDB:
        if self.username:
            user = self.users_db.get_user_by_name(self.username)
        else:
            user = self.users_db.get_user_by_guid(self.guid)
        if user:
            return user

    @property
    def user(self) -> UserModel:
        try:
            return UserModel(**self._user.model_dump())
        except AttributeError:
            raise exceptions.user_doesnt_exist

    def register(self, password: str) -> Optional["LocalUser"]:
        if not self._user:
            self.users_db.save_user(
                UserInDB(guid=str(uuid4()), username=self.username, hashed_password=get_password_hash(password))
            )
            return self

    def update(self, data: dict):
        user = self._user.model_dump()
        user.update(data)
        self.users_db.save_user(UserInDB(**user))
