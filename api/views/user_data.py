from typing import Annotated, Dict, Union

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from api.exceptions import no_data
from api.logics.local_user import LocalUser
from api.logics.tokens import get_current_user
from api.logics.user_data import write_user_data, retrieve_user_data
from models.user import UserModel

router = APIRouter()


@router.get("/me", response_model=UserModel)
async def read_users_me(
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
    return current_user


@router.post("/data", response_model=UserModel)
async def post_data(
    data: Dict[str, Union[str, int, bool]],
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
    write_user_data(current_user.username, data)
    LocalUser.users_db.save_user(user=current_user)
    return current_user


@router.get("/data")
async def get_data(current_user: Annotated[UserModel, Depends(get_current_user)]):
    data = retrieve_user_data(username=current_user.username)
    if not data:
        raise no_data
    return JSONResponse(content=data)


