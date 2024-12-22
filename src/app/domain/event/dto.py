from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.domain.event.value_objects import EventStatusEnum, EventTypeEnum


class EventDTO(BaseModel):
    class Config:
        from_attributes = True

    id: UUID
    coefficient: float
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deadline: datetime
    status: EventStatusEnum
    type: EventTypeEnum
    info: str