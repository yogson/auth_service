from asyncio import sleep
from typing import Annotated

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from api import exceptions, settings
from api.logics.local_user import LocalUser
from api.logics.login_user import LocalUserLoginProcessor

auth_router = APIRouter()


@auth_router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_login = LocalUserLoginProcessor(username=form_data.username).login(password=form_data.password)
    if not user_login or user_login._user.disabled:
        raise exceptions.bad_creds

    return {"access_token": user_login.get_access_token(), "token_type": "bearer"}


@auth_router.post("/register")
async def register(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.client_secret not in settings.APP_KEYS:
        raise exceptions.unknown_client
    user_register = LocalUser(username=form_data.username).register(password=form_data.password)
    if not user_register:
        await sleep(1)
        raise exceptions.already_exists

    return {"user": user_register.username}


