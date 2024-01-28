from fastapi import HTTPException
from starlette import status

bad_creds = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
unknown_client = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown client")
already_exists = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
no_user = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is absent")
no_data = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Data is absent for user")
bad_refresh_token = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
no_refresh_token = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing")
not_authenticated = Exception("Token can't be issued before authentication")

user_doesnt_exist = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist")


def bad_token(token_type: str):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate {token_type} token",
        headers={"WWW-Authenticate": "Bearer"},
    )
