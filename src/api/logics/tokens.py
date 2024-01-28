from datetime import timedelta, datetime
from enum import Enum
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from api import exceptions
from api.logics.local_user import LocalUser
from api.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_TTL, REFRESH_TOKEN_TTL
from models.user import UserModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class TokenType(Enum):
    access = "access"
    refresh = "refresh"


def create_token(data: dict, token_ttl: timedelta = None):
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


async def verity_access_token(token: Annotated[str, Depends(oauth2_scheme)]):
    return _verify_token(token, token_type=TokenType.access)


def _get_token(*, subject: str, token_type: str, token_ttl: int) -> str:
    data = {"sub": subject, "token_type": token_type}
    return create_token(data, token_ttl=timedelta(seconds=token_ttl))


def _verify_token(token: str, token_type: TokenType) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        guid: str = payload.get("sub")
        payload_token_type = payload.get("token_type")
        if guid is None or payload_token_type != token_type.value:
            raise exceptions.bad_token(token_type.value)
        return guid
    except JWTError:
        raise exceptions.bad_token(token_type.value)


def get_user_by_guid(guid: str):
    user = LocalUser.users_db.get_user_by_guid(guid)
    if user is None:
        raise exceptions.no_user
    return user


class TokenProcessor:
    def __init__(self, *, for_user: UserModel = None):
        self.user = for_user

    def get_access_token(self) -> str:
        return _get_token(subject=self.user.guid, token_type="access", token_ttl=ACCESS_TOKEN_TTL)

    def get_refresh_token(self) -> str:
        return _get_token(subject=self.user.guid, token_type="refresh", token_ttl=REFRESH_TOKEN_TTL)

    def verity_access_token(self, token: str):
        user_guid = _verify_token(token, TokenType.access)
        self.user = get_user_by_guid(user_guid)
        return self

    def verity_refresh_token(self, token: str):
        user_guid = _verify_token(token, TokenType.refresh)
        self.user = get_user_by_guid(user_guid)
        return self
