from datetime import timedelta, datetime
from enum import Enum
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from api import exceptions
from api.logics.local_user import LocalUser
from api.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_TTL, REFRESH_TOKEN_TTL
from models.user import UserInDB, UserModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class TokenType(Enum):
    access = "access"
    refresh = "refresh"


def create_token(data: dict, token_ttl: timedelta | None = None):
    to_encode = data.copy()
    if token_ttl:
        expire = datetime.utcnow() + token_ttl
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserModel:
    return TokenProcessor().verity_access_token(token).user


def _get_token(*, subject: str, token_type: str, token_ttl: int) -> str:
    data = {"sub": subject, "token_type": token_type}
    return create_token(data, token_ttl=timedelta(seconds=token_ttl))


class TokenProcessor:
    def __init__(self, *, for_user: UserModel = None):
        self.user = for_user

    def get_access_token(self) -> str:
        return _get_token(subject=self.user.username, token_type="access", token_ttl=ACCESS_TOKEN_TTL)

    def get_refresh_token(self) -> str:
        return _get_token(subject=self.user.username, token_type="refresh", token_ttl=REFRESH_TOKEN_TTL)

    def _verify_token(self, token: str, token_type: TokenType) -> UserModel:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            payload_token_type = payload.get("token_type")
            if username is None or payload_token_type != token_type.value:
                raise exceptions.bad_token(token_type.value)
        except JWTError:
            raise exceptions.bad_token(token_type.value)
        user = LocalUser.users_db.get_user_by_name(username)
        if user is None:
            raise exceptions.bad_token(token_type.value)
        return user

    def verity_access_token(self, token: str):
        self.user = self._verify_token(token, TokenType.access)
        return self

    def verity_refresh_token(self, token: str):
        self.user = self._verify_token(token, TokenType.refresh)
        return self
