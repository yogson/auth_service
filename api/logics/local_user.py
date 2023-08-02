from pathlib import Path

from passlib.context import CryptContext

from dao.infile_user_dao import FileUsersDAO
from models.user import UserInDB


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


class LocalUser:
    user: UserInDB
    users_db = FileUsersDAO(data_path=Path("/Users/yogson/PycharmProjects/auth_service/data/users"))

    def __init__(self, *, username: str, password: str):
        self.username = username
        self.password = password
