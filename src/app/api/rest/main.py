from contextlib import asynccontextmanager
from typing import AsyncContextManager

from fastapi import FastAPI

from app.api import rest
from app.api.rest.controllers import init_rest_api
from app.config import Config
from app.containers import Container
import uvicorn


@asynccontextmanager
async def lifespan(app_: FastAPI) -> AsyncContextManager[None]:
    Config()
    async with Container.lifespan(wireable_packages=[rest]) as container:
        app_.container = container
        yield



app = FastAPI(lifespan=lifespan)

init_rest_api(app)

