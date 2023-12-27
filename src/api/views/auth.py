from asyncio import sleep
from typing import Annotated

from fastapi import Depends, APIRouter, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request

from api import exceptions, settings
from api.exceptions import no_refresh_token, bad_refresh_token
from api.logics.local_user import LocalUser
from api.logics.login_user import LocalUserLoginProcessor
from api.logics.tokens import TokenProcessor
from api.settings import LIMIT_REGISTER, LIMIT_LOGIN
from api.limiters import limiter

auth_router = APIRouter()


@auth_router.post("/login")
@limiter.limit(LIMIT_LOGIN)
async def login(request: Request, response: Response, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = LocalUserLoginProcessor(username=form_data.username).login(password=form_data.password)
    if not user or user.disabled:
        raise exceptions.bad_creds
    token_processor = TokenProcessor(for_user=user)
    response.set_cookie(
        key="refresh_token", value=token_processor.get_refresh_token(), httponly=True, secure=True, samesite="lax"
    )
    return {"access_token": token_processor.get_access_token(), "token_type": "Bearer"}


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


@auth_router.post("/refresh")
async def refresh_token(response: Response, refresh_token: str = Cookie(None)):
    if refresh_token is None:
        raise no_refresh_token
    token_processor = TokenProcessor().verity_refresh_token(refresh_token)
    if not token_processor.user:
        raise bad_refresh_token
    return {"access_token": token_processor.get_access_token(), "token_type": "Bearer"}
