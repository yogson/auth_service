import datetime
import json
from functools import cached_property
from pathlib import Path
from typing import Optional

from dao.abstract_user_dao import AbstractUsersDAO
from models.user import UserInDB
from utils.common import get_utcnow_timestamp


class FileUsersDAO(AbstractUsersDAO):

    def __init__(self, file_obj: Path):
        self.file = file_obj
        self.__objects = None  # type: list

    @property
    def _objects(self) -> list:
        if not self.__objects:
            self.__objects = json.loads(self.file.read_text())
        return self.__objects

    @_objects.setter
    def _objects(self, data: list):
        self.__objects = data

    def _save(self, data: list[dict]):
        self.file.write_text(json.dumps(data, indent=2))

    def get_user_by_name(self, username: str) -> Optional[UserInDB]:
        for user in filter(lambda x: x["username"] == username, self._objects):
            return UserInDB(**user)

    def save_user(self, user: UserInDB):
        objects = self._objects
        user_data = dict(user)
        user_data["updated_at"] = get_utcnow_timestamp()
        all(map(lambda x: objects.pop(objects.index(x)), filter(lambda r: r["username"] == user.username, objects)))
        objects.append(user_data)
        self._save(self._objects)

