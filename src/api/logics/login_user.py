from datetime import timedelta
from typing import Optional

from api.logics.local_user import LocalUser, verify_password
from api.logics.tokens import create_access_token
from api.settings import ACCESS_TOKEN_TTL
from utils.common import get_utcnow_timestamp


class LocalUserLoginProcessor(LocalUser):

    def __init__(self, *, username: str):
        super().__init__(username=username)
        self.authenticated = False

    def login(self, password: str) -> Optional["LocalUserLoginProcessor"]:
        if self.authenticate(password):
            self._user.last_login = get_utcnow_timestamp()
            self.users_db.save_user(self._user, update_ts=False)
            return self

    def get_access_token(self):
        if self.authenticated:
            data = {"sub": self._user.username}
            return create_access_token(data, token_ttl=timedelta(seconds=ACCESS_TOKEN_TTL))

    def authenticate(self, password: str) -> bool:
        if self._user and verify_password(password, self._user.hashed_password):
            self.authenticated = True
        return self.authenticated

