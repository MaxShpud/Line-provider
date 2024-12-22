from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.models.enums.bet.status import BetStatus
from app.models.enums.event.statuses import EventStatusEnum


class CreateBetSchema(BaseModel):
    event_id: UUID
    amount: Decimal

class RetrieveBetSchema(BaseModel):
    class Config:
        from_attributes = True

    id: int
    event_id: UUID
    amount: Decimal
    status: BetStatus
    created_at: datetime

    @classmethod
    def from_orm(cls, obj):
        return super().from_orm(obj)

class RetrieveBetsSchema(BaseModel):
    bets: list[RetrieveBetSchema]


class UpdateBetStatusSchema(BaseModel):
    event_id: UUID
    status:  EventStatusEnum
