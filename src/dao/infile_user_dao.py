import json
from pathlib import Path
from typing import Optional

from dao.abstract_user_dao import AbstractUsersDAO
from models.user import UserInDB
from utils.common import get_utcnow_timestamp


class FileUser:
    def __init__(self, base_path: Path, username: str, guid: str = None):
        self.base_path = base_path
        self.username = username
        self.guid = guid
        self.is_new = False

    @property
    def user_path(self) -> Path:
        return self.base_path / self.username[0].capitalize()

    @property
    def user_file(self) -> Path:
        return self.user_path / f"{self.username}.json"

    def save(self, data: dict) -> 'FileUser':
        try:
            if not self.user_file.exists():
                self.is_new = True
            self.user_file.write_text(json.dumps(data))
        except FileNotFoundError:
            if not self.user_path.exists():
                self.user_path.mkdir(parents=True, exist_ok=True)
                self.save(data)
        return self

    def read(self) -> Optional[dict]:
        try:
            return json.loads(self.user_file.read_text())
        except FileNotFoundError:
            return


class FileUsersDAO(AbstractUsersDAO):
    GUID_INDEX_FILE = 'index.jsonl'

    def __init__(self, data_path: Path):
        self.data_path = data_path
        self._check_path()

    @property
    def _guid_index_file(self) -> Path:
        return self.data_path / self.GUID_INDEX_FILE

    def _get_username_by_guid(self, guid: str):
        with open(self._guid_index_file) as f:
            for line in f:
                record = json.loads(line)
                if record:
                    if record.get("guid") == guid:
                        return record.get("username")

    def _append_guid_index(self, guid: str, username: str):
        with open(self._guid_index_file, "a") as f:
            f.write(json.dumps({"guid": guid, "username": username}) + "\n")

    def _check_path(self):
        if not self.data_path.exists():
            if self.data_path.is_dir():
                self.data_path.mkdir(parents=True, exist_ok=True)
                (Path(self.data_path) / self.GUID_INDEX_FILE).touch(exist_ok=True)

    def _save(self, user: UserInDB):
        user = FileUser(base_path=self.data_path, username=user.username, guid=user.guid).save(dict(user))
        if user.is_new:
            self._append_guid_index(user.guid, user.username)

    def get_user_by_guid(self, guid: str) -> Optional[UserInDB]:
        username = self._get_username_by_guid(guid)
        if username:
            return self.get_user_by_name(username=username)

    def get_user_by_name(self, username: str) -> Optional[UserInDB]:
        user_file = FileUser(base_path=self.data_path, username=username)
        user = user_file.read()
        if user:
            return UserInDB(**user)

    def save_user(self, user: UserInDB, update_ts=True):
        user.updated_at = get_utcnow_timestamp() if update_ts else user.updated_at
        self._save(user)
