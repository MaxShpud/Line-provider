from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, TypeAdapter

from app.domain.event.value_objects import EventStatusEnum, EventTypeEnum


class EventOutputDTO(BaseModel):
    class Config:
        from_attributes = True

    id: UUID
    coefficient: float
    deadline: datetime
    status: EventStatusEnum
    type: EventTypeEnum
    info: str


class EventRetrieveInputDTO(BaseModel):
    event_id: UUID

class EventUpdateInputDTO(BaseModel):
    id: UUID
    coefficient: float
    deadline: datetime
    status: EventStatusEnum
    type: EventTypeEnum
    info: str

EventListOutputDTO = TypeAdapter(list[EventOutputDTO])