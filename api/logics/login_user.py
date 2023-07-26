from datetime import timedelta
from functools import cached_property
from typing import Optional

from api.logics.local_user import LocalUser, verify_password
from api.logics.tokens import create_access_token
from api.settings import ACCESS_TOKEN_TTL
from utils.common import get_utcnow_timestamp


class LocalUserLoginProcessor(LocalUser):

    def login(self) -> Optional["LocalUserLoginProcessor"]:
        if self.authenticated:
            self.user.last_login = get_utcnow_timestamp()
            self.users_db.save_user(self.user)
            return self

    def get_access_token(self):
        if self.authenticated:
            data = {"sub": self.user.username}
            return create_access_token(data, token_ttl=timedelta(seconds=ACCESS_TOKEN_TTL))

    @cached_property
    def authenticated(self) -> bool:
        return self._authenticate()

    def _authenticate(self):
        user = self.users_db.get_user_by_name(self.username)
        if not user or not verify_password(self.password, user.hashed_password):
            return False
        self.user = user
        return True

