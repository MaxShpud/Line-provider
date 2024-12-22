from typing import Optional, Any

from fastapi import Depends

from app.schemas.pydantic.bet.schemas import CreateBetSchema
from app.services.bet import BetService
from app.services.redis import RedisService


class EventRouter(object):
    tags = ("Events",)

    def __init__(self, app):
        self.app = app

    def configure_routes(self):
        self.app.get('/events',
                     tags=self.tags,
                     summary='Event',
                     response_model=None)(self.retrieve_list)

    @staticmethod
    async def retrieve_list(
            redisService: RedisService = Depends()
    ):
        return await redisService.get_all_data()


