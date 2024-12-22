from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

router = APIRouter()

@router.get('/heathcheck')
@inject
async def heath_check():
    return {"status": "ok"}