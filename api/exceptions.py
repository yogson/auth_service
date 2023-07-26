from fastapi import HTTPException
from starlette import status

bad_creds = HTTPException(status_code=400, detail="Incorrect username or password")
unknown_client = HTTPException(status_code=400, detail="Unknown client")
already_exists = HTTPException(status_code=400, detail="User already exists")
bad_token =  HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate the token",
        headers={"WWW-Authenticate": "Bearer"},
    )