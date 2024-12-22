from uuid import UUID

from pydantic import BaseModel

from app.domain.event.value_objects import EventStatusEnum


class EventInputDTO(BaseModel):
    class Config:
        from_attributes = True

    event_id: UUID
    status:  EventStatusEnum
