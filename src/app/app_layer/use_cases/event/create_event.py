from datetime import datetime

from app.app_layer.interfaces.unit_of_work.sql import IUnitOfWork
from app.app_layer.use_cases.event.dto import EventOutputDTO
from app.domain.event.entity import Event
from app.domain.event.value_objects import EventTypeEnum, EventStatusEnum
from app.infrastructure.events.redis import RedisService


class CreateEventUseCase:

    def __init__(self,
                 uow: IUnitOfWork,
                 redis_service: RedisService
                 ) -> None:
        self._uow = uow
        self._redis_service = redis_service

    async def create_event(
                self,
               coefficient: float,
               deadline: datetime,
               status: EventStatusEnum,
               event_type: EventTypeEnum,
               info: str,

    ) -> EventOutputDTO:
        """
        Creates a event.
        """
        return await self._create(coefficient, deadline, status, event_type, info)

    async def _create(self,
                      coefficient: float,
                      deadline: datetime,
                      status: EventStatusEnum,
                      event_type: EventTypeEnum,
                      info: str
    ) -> EventOutputDTO:
        event = Event.create(coefficient=coefficient,
                             deadline=deadline,
                             status=status,
                             event_type=event_type,
                             info=info)

        await self._redis_service.put_data(key=str(event.id), data=event.to_dict(), deadline=deadline)

        async with self._uow(autocommit=True):
            await self._uow.event.create(event=event)

        return EventOutputDTO.model_validate(event)