from asyncio import sleep
from typing import Annotated

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request

from api import exceptions, settings
from api.logics.local_user import LocalUser
from api.logics.login_user import LocalUserLoginProcessor
from api.settings import LIMIT_REGISTER, LIMIT_LOGIN
from api.limiters import limiter

auth_router = APIRouter()


@auth_router.post("/login")
@limiter.limit(LIMIT_LOGIN)
async def login(request: Request, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_login = LocalUserLoginProcessor(username=form_data.username).login(password=form_data.password)
    if not user_login or user_login.user.disabled:
        raise exceptions.bad_creds
    return {"access_token": user_login.get_access_token(), "token_type": "bearer"}


@auth_router.post("/register")
@limiter.limit(LIMIT_REGISTER)
async def register(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.client_secret not in settings.APP_KEYS:
        raise exceptions.unknown_client
    user_register = LocalUser(username=form_data.username).register(password=form_data.password)
    if not user_register:
        await sleep(1)
        raise exceptions.already_exists

    return {"user": user_register.username}


