import logging
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.datastructures import MutableHeaders
from pydantic.v1 import BaseSettings

__all__ = ('configure_app_middlewares',)

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    allow_origins: list = ["http://localhost:5173"]
    allow_credentials: bool = True
    allow_methods: list = ["POST", "GET", "PUT", "DELETE"]
    allow_headers: list = ["*"]


settings = Settings()


def configure_app_middlewares(application: FastAPI) -> None:
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allow_origins,
        allow_credentials=settings.allow_credentials,
        allow_methods=settings.allow_methods,
        allow_headers=settings.allow_headers,
    )
