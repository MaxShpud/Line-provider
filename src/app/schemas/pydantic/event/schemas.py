from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.enums.event.statuses import EventStatusEnum, EventTypeEnum


class EventSchema(BaseModel):
    class Config:
        from_attributes = True
        populate_by_name = True

    id: UUID
    coefficient: float
    deadline: datetime
    status: EventStatusEnum
    type: EventTypeEnum
    info: str