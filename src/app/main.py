from fastapi import FastAPI
import uvicorn

from app.core.app_routers import configure_app_routes
from app.core.app_configs import configure_app_configs
from app.core.app_middlewares import configure_app_middlewares

__all__ = (
    'get_ctx',
)
app = FastAPI(title='bet-maker', prefix='/v1/bet-maker')

ctx = dict()

configure_app_configs(app, ctx)
configure_app_middlewares(app)
configure_app_routes(app)


def get_ctx():
    return ctx

