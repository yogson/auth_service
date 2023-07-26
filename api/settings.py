PATH_PREFIX = 'api'
API_VER = '0.1'

PATH = f'/{PATH_PREFIX}/v{API_VER}'

SECRET_KEY = "OMGSUPERSECRET!"
APP_KEYS = ()
ALGORITHM = "HS512"
ACCESS_TOKEN_TTL = 1800

try:
    from api.local_settings import *
except:
    pass
