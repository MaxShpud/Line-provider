from fastapi import FastAPI

__all__ = ('configure_app_configs',)

from app.configs import initialize_configs


def configure_app_configs(application: FastAPI, ctx: dict) -> None:
    initialize_configs(application, ctx=ctx)
