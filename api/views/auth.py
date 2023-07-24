from datetime import timedelta
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from api import exceptions
from api.logics.tokens import create_access_token
from api.settings import ACCESS_TOKEN_TTL
from dao.infile_user_dao import FileUsersDAO

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users_db = users = FileUsersDAO(file_obj=Path("/Users/yogson/PycharmProjects/auth_service/tests/users.json"))


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = users_db.get_user_by_name(form_data.username)
    if not user:
        raise exceptions.bad_creds
    if not verify_password(form_data.password, user.hashed_password):
        raise exceptions.bad_creds

    access_token = create_access_token(
        data={"sub": user.username}, token_ttl=timedelta(seconds=ACCESS_TOKEN_TTL)
    )

    return {"access_token": access_token, "token_type": "bearer"}