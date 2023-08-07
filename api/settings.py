from os import environ

PATH_PREFIX = 'api'
API_VER = '0.1'

PATH = f'/{PATH_PREFIX}/v{API_VER}'

SECRET_KEY = "OMGSUPERSECRET!"
APP_KEYS = ()
ALGORITHM = "HS512"
ACCESS_TOKEN_TTL = 1800

USER_DATA_STORE = environ.get("USER_DATA_STORE")
USERS_STORE = environ.get("USERS_STORE")

try:
    from api.local_settings import *
except:
    pass
