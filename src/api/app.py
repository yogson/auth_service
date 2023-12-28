from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from api.limiters import limiter
from api.settings import ORIGINS


def _set_cors_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def _set_limiters(app: FastAPI):
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


class App:
    app: FastAPI = None

    def __new__(cls, *_, **__):
        return cls.__call__()

    @classmethod
    def __call__(cls) -> FastAPI:
        if not cls.app:
            from api.routes import root_router

            cls.app = FastAPI()
            cls.app.include_router(root_router)
            _set_limiters(cls.app)
            _set_cors_middleware(cls.app)
        return cls.app
