from fastapi import APIRouter

from app.api.rest import public

public_api = APIRouter()

public_api.include_router(public.v1.event.controllers.router,
                          tags=["Events"],
                          prefix="/v1/event")
public_api.include_router(public.v1.general.controllers.router,
                          tags=["General"],
                          prefix="/v1/general")