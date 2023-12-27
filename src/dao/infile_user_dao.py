import json
from pathlib import Path
from typing import Optional

from dao.abstract_user_dao import AbstractUsersDAO
from models.user import UserInDB
from utils.common import get_utcnow_timestamp


class FileUser:
    def __init__(self, base_path: Path, username: str):
        self.base_path = base_path
        self.username = username

    @property
    def user_path(self) -> Path:
        return self.base_path / self.username[0].capitalize()

    @property
    def user_file(self) -> Path:
        return self.user_path / f"{self.username}.json"

    def save(self, data: dict):
        try:
            self.user_file.write_text(json.dumps(data))
        except FileNotFoundError:
            if not self.user_path.exists():
                self.user_path.mkdir(parents=True, exist_ok=True)
                self.save(data)

    def read(self) -> Optional[dict]:
        try:
            return json.loads(self.user_file.read_text())
        except FileNotFoundError:
            return


class FileUsersDAO(AbstractUsersDAO):
    def __init__(self, data_path: Path):
        self.data_path = data_path
        self._check_path()

    def _check_path(self):
        if not self.data_path.exists():
            if self.data_path.is_dir():
                self.data_path.mkdir(parents=True, exist_ok=True)

    def _save(self, username: str, data: dict):
        FileUser(base_path=self.data_path, username=username).save(data)

    def get_user_by_name(self, username: str) -> Optional[UserInDB]:
        user_file = FileUser(base_path=self.data_path, username=username)
        user = user_file.read()
        if user:
            return UserInDB(**user)

    def save_user(self, user: UserInDB, update_ts=True):
        user_data = dict(user)
        user_data["updated_at"] = get_utcnow_timestamp() if update_ts else user_data["updated_at"]
        self._save(username=user.username, data=user_data)
