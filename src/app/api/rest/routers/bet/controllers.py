from typing import Optional, Any

from fastapi import Depends, Query

from app.models.enums.bet.status import BetStatus
from app.schemas.pydantic.bet.schemas import CreateBetSchema, RetrieveBetSchema, RetrieveBetsSchema, \
    UpdateBetStatusSchema
from app.services.bet import BetService


class BetRouter(object):
    tags = ("Bets",)

    def __init__(self, app):
        self.app = app

    def configure_routes(self):
        self.app.get('/bet/{bet_id}',
                     tags=self.tags,
                     summary='Bet',
                     response_model=RetrieveBetSchema)(self.retrieve)
        self.app.get('/bets',
                     tags=self.tags,
                     summary='Bets',
                     response_model=RetrieveBetsSchema)(self.list)
        self.app.post('/bet',
                      tags=self.tags,
                      summary='Bet',
                      response_model=None)(self.create)
        self.app.put('/bet/status',
                     tags=self.tags,
                     summary='Bet',
                     response_model=None)(self.update_status)


    @staticmethod
    async def retrieve(
            bet_id: int,
            betService: BetService = Depends()
    )-> RetrieveBetSchema:
        return await betService.retrieve(bet_id=bet_id)

    @staticmethod
    async def create(
            data: CreateBetSchema,
            betService: BetService = Depends()
    ):
        try:
            await betService.create(event_id=data.event_id,
                                    amount=data.amount)
        except Exception as e:
            raise e
    @staticmethod
    async def list(
            status: Optional[BetStatus] = Query(None, description="Filter bets by status"),
            betService: BetService = Depends()
    )-> RetrieveBetsSchema:
        return await betService.list(filter_status=status)

    @staticmethod
    async def update_status(
            data: UpdateBetStatusSchema,
            betService: BetService = Depends()
    ):
        try:
            await betService.update_status_by_event_id(
                event_id=data.event_id,
                status=data.status.value
            )
        except Exception as e:
            raise e