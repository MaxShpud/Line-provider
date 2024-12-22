from datetime import datetime
from uuid import UUID

from app.app_layer.interfaces.clients.bets.bet import IBetClient
from app.app_layer.interfaces.clients.bets.dto import EventInputDTO
from app.app_layer.interfaces.unit_of_work.sql import IUnitOfWork
from app.app_layer.use_cases.event.dto import EventUpdateInputDTO, EventOutputDTO
from app.domain.event.entity import Event
from app.domain.event.value_objects import EventStatusEnum, EventTypeEnum
from app.infrastructure.events.redis import RedisService


class UpdateEventUseCase:
    """
    Responsible for retrieving a event.
    """

    def __init__(self, uow: IUnitOfWork,
                 redis_service: RedisService,
                 bet_client: IBetClient,
    ) -> None:
        self._uow = uow
        self._redis_service = redis_service
        self._bet_client = bet_client

    async def execute(self,
                      event_id: UUID,
                      coefficient: float,
                       deadline: datetime,
                       status: EventStatusEnum,
                       event_type: EventTypeEnum,
                       info: str
    ) -> EventOutputDTO:
        """
        Executes the use case  by updating the event. Returns the retrieved
        event as a EventOutputDTO object.
        """
        event = Event.update(event_id=event_id,
                             coefficient=coefficient,
                             deadline=deadline,
                             status=status,
                             event_type=event_type,
                             info=info)

        async with self._uow(autocommit=True):
            prev_event = await self._uow.event.retrieve(event_id=event_id)
            upd_event = await self._uow.event.update(event=event)

        await self._redis_service.put_data(key=str(event.id), data=event.to_dict(), deadline=event.deadline)

        if prev_event.status != status:
            bet_data = EventInputDTO(
                event_id=event_id,
                status=status,
            )
            await self._bet_client.update_bet(
                data=bet_data,
            )
        return EventOutputDTO.model_validate(upd_event)