from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    last_login: int | None = None
    updated_at: int | None = None
    disabled: bool | None = None


class UserProperties(BaseModel):
    email: str | None = None
    full_name: str | None = None


class UserModel(UserBase, UserProperties):
    pass


class UserInDB(UserModel):
    hashed_password: str
