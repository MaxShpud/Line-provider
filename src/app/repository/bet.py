from decimal import Decimal
from typing import Union
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends
from app.models.bet import Bet
from app.models.enums.bet.status import BetStatus
from app.configs.database import get_db
from app.models.enums.event.statuses import EventStatusEnum


class BetRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db


    async def create(self, event_id: UUID, amount: Decimal) -> Bet:
        bet = Bet(event_id=event_id, amount=amount)
        try:
            self.db.add(bet)
            await self.db.commit()
            await self.db.refresh(bet)
            return bet
        except Exception:
            await self.db.rollback()
            raise

    async def retrieve(self, bet_id: int) -> Bet:
        return await self.db.get(Bet, bet_id)

    async def list(self, filter_status: Union[BetStatus, None]):
        stmt = select(Bet)
        if filter_status is not None:
            stmt = stmt.filter(Bet.status == filter_status)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update_status_by_event_id(self, event_id: UUID, status: EventStatusEnum) -> None:
        """
        """
        stmt = select(Bet).filter(Bet.event_id == event_id)
        result = await self.db.execute(stmt)
        bets_to_update = result.scalars().all()

        for bet in bets_to_update:
            bet.status = status

        try:
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise