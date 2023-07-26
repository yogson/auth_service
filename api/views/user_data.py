from typing import Annotated

from fastapi import APIRouter, Depends

from api.logics.local_user import LocalUser
from api.logics.tokens import get_current_user
from models.user import UserModel

router = APIRouter()


@router.get("/me", response_model=UserModel)
async def read_users_me(
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
    return current_user


@router.post("/data", response_model=UserModel)
async def read_users_me(
    data: dict,
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
    current_user.data = data
    LocalUser.users_db.save_user(user=current_user)
    return current_user


