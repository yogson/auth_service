from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from api import exceptions
from api.logics.login_user import UserLoginProcessor

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_login = UserLoginProcessor(username=form_data.username, password=form_data.password).login()
    if not user_login:
        raise exceptions.bad_creds

    return {"access_token": user_login.get_access_token(), "token_type": "bearer"}