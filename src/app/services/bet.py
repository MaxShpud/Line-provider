from decimal import Decimal
from typing import Union
from uuid import UUID

from fastapi import Depends

from app.models.enums.bet.status import BetStatus
from app.models.enums.event.statuses import EventStatusEnum
from app.repository.bet import BetRepository
from app.schemas.pydantic.bet.schemas import RetrieveBetSchema, RetrieveBetsSchema
from app.services.redis import RedisService


class BetService:
    betRepository = BetRepository()

    def __init__(self,
                 betRepository: BetRepository = Depends(),
                 redisService: RedisService = Depends()
                 ) -> None:
        self.betRepository = betRepository
        self.redisService = redisService

    async def create(self,
               event_id: UUID,
               amount: Decimal
    ) -> None:
        await self.betRepository.create(event_id=event_id, amount=amount)

    async def retrieve(self,
                       bet_id: int,
    ) -> RetrieveBetSchema:
        bet = await self.betRepository.retrieve(bet_id)
        return RetrieveBetSchema.from_orm(bet)

    async def list(self, filter_status: Union[BetStatus, None] ) -> RetrieveBetsSchema:
        bets = [
            RetrieveBetSchema.from_orm(bet)
            for bet in await self.betRepository.list(filter_status=filter_status)
        ]
        return RetrieveBetsSchema(bets=bets)

    async def update_status_by_event_id(self,
                     event_id: UUID,
                     status: EventStatusEnum,
    ) -> None:
        await self.betRepository.update_status_by_event_id(event_id=event_id, status=status)
