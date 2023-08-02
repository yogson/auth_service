from asyncio import sleep
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, OAuth2PasswordRequestFormStrict

from api import exceptions, settings
from api.logics.login_user import LocalUserLoginProcessor
from api.logics.register_user import LocalUserRegister

router = APIRouter()


@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_login = LocalUserLoginProcessor(username=form_data.username, password=form_data.password).login()
    if not user_login or user_login.user.disabled:
        raise exceptions.bad_creds

    return {"access_token": user_login.get_access_token(), "token_type": "bearer"}


@router.post("/register")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if form_data.client_secret not in settings.APP_KEYS:
        raise exceptions.unknown_client
    user_register = LocalUserRegister(username=form_data.username, password=form_data.password).register()
    if not user_register:
        await sleep(1)
        raise exceptions.already_exists

    return {"user": user_register.user.username}


