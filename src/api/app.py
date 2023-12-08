from fastapi import FastAPI, APIRouter

from api.settings import PATH
from api.views.auth import auth_router
from api.views.user import user_router
from api.views.user_data import data_router

app = FastAPI()

user_router.include_router(data_router)

root_router = APIRouter(
    prefix=PATH
)

root_router.include_router(
    auth_router,
    prefix="/auth"
)

root_router.include_router(
    user_router,
    prefix="/user"
)

app.include_router(root_router)