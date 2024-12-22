from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, field_validator

from app.domain.event.value_objects import EventStatusEnum, EventTypeEnum

class EventCoefficientViewModel(BaseModel):
    coefficient: float

    @field_validator("coefficient")
    @classmethod
    def validate_coefficient(cls, value: float) -> float:
        if round(value, 2) != value:
            raise ValueError("Coefficient must have at most two decimal places.")
        return value

class EventViewModel(EventCoefficientViewModel):
    class Config:
        from_attributes = True
        populate_by_name = True

    id: UUID

    deadline: datetime
    status: EventStatusEnum
    type: EventTypeEnum
    info: str


class CreateEventViewModel(EventCoefficientViewModel):
    deadline: datetime
    status: EventStatusEnum
    type: EventTypeEnum
    info: str

class UpdateEventViewModel(EventCoefficientViewModel):
    id: UUID
    deadline: datetime
    status: EventStatusEnum
    type: EventTypeEnum
    info: str

class EventListViewModel(BaseModel):
    events: list[EventViewModel]