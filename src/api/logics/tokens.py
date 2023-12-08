from datetime import timedelta, datetime
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from api import exceptions
from api.logics.local_user import LocalUser
from api.settings import SECRET_KEY, ALGORITHM
from models.user import UserInDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict, token_ttl: timedelta | None = None):
    to_encode = data.copy()
    if token_ttl:
        expire = datetime.utcnow() + token_ttl
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserInDB:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise exceptions.bad_token
    except JWTError:
        raise exceptions.bad_token
    user = LocalUser.users_db.get_user_by_name(username)
    if user is None:
        raise exceptions.bad_token
    return user
