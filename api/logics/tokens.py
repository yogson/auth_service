from datetime import timedelta, datetime

from jose import jwt

from api.settings import SECRET_KEY, ALGORITHM


def create_access_token(data: dict, token_ttl: timedelta | None = None):
    to_encode = data.copy()
    if token_ttl:
        expire = datetime.utcnow() + token_ttl
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
