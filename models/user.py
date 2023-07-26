from pydantic import BaseModel


class UserModel(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    last_login: int | None = None
    updated_at: int | None = None
    data: dict | None = None


class UserInDB(UserModel):
    hashed_password: str
