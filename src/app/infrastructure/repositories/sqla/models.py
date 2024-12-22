from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy import func, Index, Text, Float, Numeric
from sqlalchemy.orm import (
    declarative_mixin,
    mapped_column,
    Mapped,
)

from app.infrastructure.repositories.sqla.base import Base
from app.domain.event.value_objects import EventStatusEnum, EventTypeEnum


@declarative_mixin
class TimestampMixin:
    timestamp = Annotated[
        datetime,
        mapped_column(
            nullable=False,
            default=datetime.utcnow(),
            server_default=func.CURRENT_TIMESTAMP(),
        ),
    ]

    created_at: Mapped[timestamp]
    updated_at: Mapped[timestamp] = mapped_column(
        onupdate=datetime.utcnow,
        server_onupdate=func.CURRENT_TIMESTAMP(),
    )


class Event(TimestampMixin, Base):
    __tablename__ = "event"

    id: Mapped[UUID] = mapped_column(
        sa.UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    coefficient: Mapped[float] = mapped_column(Numeric(precision=10, scale=2), nullable=False)
    deadline: Mapped[datetime] = mapped_column(
            nullable=False,
            default=datetime.utcnow(),
            server_default=func.CURRENT_TIMESTAMP(),
        )
    status: Mapped[EventStatusEnum] = mapped_column(
        default=EventStatusEnum.UNFINISHED,
        server_default=EventStatusEnum.UNFINISHED.value,
    )
    type: Mapped[EventTypeEnum] = mapped_column(
        default=EventTypeEnum.NONE,
        server_default=EventTypeEnum.NONE.value,
    )
    info: Mapped[str] = mapped_column(Text, nullable=True)

