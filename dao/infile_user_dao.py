import json
from functools import cached_property
from pathlib import Path
from typing import Optional

from dao.abstract_user_dao import AbstractUsersDAO
from models.user import UserInDB


class FileUsersDAO(AbstractUsersDAO):

    def __init__(self, file_obj: Path):
        self.file = file_obj

    @cached_property
    def objects(self):
        return json.loads(self.file.read_text())

    def get_user_by_name(self, username: str) -> Optional[UserInDB]:
        for user in filter(lambda x: x["username"] == username, self.objects):
            return UserInDB(**user)
