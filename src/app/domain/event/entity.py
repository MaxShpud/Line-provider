import uuid
from datetime import datetime

from app.domain.event.dto import EventDTO
from app.domain.event.value_objects import EventStatusEnum, EventTypeEnum


class Event:
    """
    Represents event and provides methods to modify and manage the event
    data and change the event status.
    """

    def __init__(
            self,
            data: EventDTO,
    ) -> None:
        self.id = data.id
        self.coefficient = data.coefficient
        self.created_at = data.created_at
        self.updated_at = data.updated_at
        self.deadline = data.deadline
        self.status = data.status
        self.type = data.type
        self.info = data.info

    @classmethod
    def create(cls,
               coefficient: float,
               deadline: datetime,
               status: EventStatusEnum,
               event_type: EventTypeEnum,
               info: str
    ) -> "Event":
        """Creates a new event."""
        return cls(
            data=EventDTO(
                id=uuid.uuid4(),
                coefficient=coefficient,
                created_at=datetime.now(),
                deadline=deadline,
                status=status,
                type=event_type,
                info=info,
            )
        )

    @classmethod
    def update(cls,
               event_id: uuid.UUID,
               coefficient: float,
               deadline: datetime,
               status: EventStatusEnum,
               event_type: EventTypeEnum,
               info: str
               ) -> "Event":
        """Updates event."""
        if status in [EventStatusEnum.WON, EventStatusEnum.LOST]:
            deadline = datetime.now()
        return cls(
            data=EventDTO(
                id=event_id,
                coefficient=coefficient,
                updated_at=datetime.now(),
                deadline=deadline,
                status=status,
                type=event_type,
                info=info,
            )
        )

    def to_dict(self):
        """Convert the event to a dictionary that can be serialized to JSON."""
        return {
            "id": str(self.id),
            "coefficient": self.coefficient,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "status": self.status.name,
            "type": self.type.name,
            "info": self.info
        }