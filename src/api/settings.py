from os import environ

PATH_PREFIX = "api"
API_VER = "0.1"

PATH = f"/{PATH_PREFIX}/v{API_VER}"

SECRET_KEY = environ.get("SECRET_KEY")
APP_KEYS = environ.get("APP_KEYS").split(",")
ALGORITHM = "HS512"
ACCESS_TOKEN_TTL = 600
REFRESH_TOKEN_TTL = 10800
ORIGINS = environ.get("ORIGINS").split(",")

USER_DATA_STORE = environ.get("USER_DATA_STORE")
USERS_STORE = environ.get("USERS_STORE")

LIMIT_REGISTER = "2/minute"
LIMIT_LOGIN = "10/minute"

try:
    from api.local_settings import *
except:
    pass
