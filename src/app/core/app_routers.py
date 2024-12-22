from fastapi import FastAPI
from app.api.rest.routers.bet.controllers import BetRouter


__all__ = ('configure_app_routes',)

from app.api.rest.routers.event.controllers import EventRouter

routers = [
    BetRouter,
    EventRouter
]


def configure_app_routes(application: FastAPI) -> None:
    for router in routers:
        new_router = router(application)
        new_router.configure_routes()
