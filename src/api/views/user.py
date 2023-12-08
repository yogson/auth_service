from fastapi import Depends, APIRouter

from api.logics.local_user import LocalUser
from api.logics.tokens import get_current_user
from models.user import UserModel, UserProperties

user_router = APIRouter()


@user_router.get("/me", response_model=UserModel)
async def read_me(current_user: UserModel = Depends(get_current_user)):
    return current_user


@user_router.patch("/me", response_model=UserModel)
async def read_me(update: UserProperties, current_user: UserModel = Depends(get_current_user)):
    user_dict = current_user.model_dump()
    user_dict.update(update.model_dump())
    LocalUser(username=current_user.username).update(user_dict)
    return UserModel(**user_dict)

