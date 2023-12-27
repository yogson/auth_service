from typing import Optional

from api.logics.local_user import LocalUser, verify_password
from models.user import UserModel
from utils.common import get_utcnow_timestamp


class LocalUserLoginProcessor(LocalUser):
    def __init__(self, *, username: str):
        super().__init__(username=username)
        self.authenticated = False

    def login(self, password: str) -> Optional[UserModel]:
        if self.authenticate(password):
            self._user.last_login = get_utcnow_timestamp()
            self.users_db.save_user(self._user, update_ts=False)
            return self.user

    def authenticate(self, password: str) -> bool:
        if self._user and verify_password(password, self._user.hashed_password):
            self.authenticated = True
        return self.authenticated
