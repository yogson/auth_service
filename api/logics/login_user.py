from datetime import timedelta
from functools import cached_property
from pathlib import Path
from typing import Optional

from passlib.context import CryptContext

from api.logics.tokens import create_access_token
from api.settings import ACCESS_TOKEN_TTL
from dao.infile_user_dao import FileUsersDAO
from models.user import UserInDB
from utils.common import get_utcnow_timestamp

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users_db = users = FileUsersDAO(file_obj=Path("/Users/yogson/PycharmProjects/auth_service/tests/users.json"))


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


class UserLoginProcessor:
    user: UserInDB

    def __init__(self, *, username: str, password: str):
        self.username = username
        self.password = password

    def login(self) -> Optional["UserLoginProcessor"]:
        if self.authenticated:
            self.user.last_login = get_utcnow_timestamp()
            users_db.save_user(self.user)
            return self

    def get_access_token(self):
        if self.authenticated:
            data = {"sub": self.user.username}
            return create_access_token(data, token_ttl=timedelta(seconds=ACCESS_TOKEN_TTL))

    @cached_property
    def authenticated(self) -> bool:
        return self._authenticate()

    def _authenticate(self):
        user = users_db.get_user_by_name(self.username)
        if not user or not verify_password(self.password, user.hashed_password):
            return False
        self.user = user
        return True

