from fastapi import FastAPI, APIRouter

from api.settings import PATH
from api.views import auth, user_data

app = FastAPI()

root_router = APIRouter(
    prefix=PATH
)

root_router.include_router(
    auth.router,
    prefix="/auth"
)

root_router.include_router(
    user_data.router,
    prefix="/user"
)

app.include_router(root_router)