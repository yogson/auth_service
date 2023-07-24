from pydantic import BaseModel


class UserModel(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(UserModel):
    hashed_password: str
