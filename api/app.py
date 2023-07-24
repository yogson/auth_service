from fastapi import FastAPI, APIRouter

from api.settings import PATH
from api.views import auth

app = FastAPI()

root_router = APIRouter(
    prefix=PATH
)

root_router.include_router(
    auth.router,
    prefix="/auth"
)

app.include_router(root_router)