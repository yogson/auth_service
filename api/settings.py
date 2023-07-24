PATH_PREFIX = 'api'
API_VER = '0.1'

PATH = f'/{PATH_PREFIX}/v{API_VER}'

SECRET_KEY = "OMGSUPERSECRET!"
ALGORITHM = "HS256"
ACCESS_TOKEN_TTL = 1800

try:
    import local_settings
except ImportError:
    pass
