from app.app_layer.interfaces.unit_of_work.sql import IUnitOfWork
from app.app_layer.use_cases.event.dto import EventRetrieveInputDTO, EventOutputDTO


class RetrieveEventUseCase:
    """
    Responsible for retrieving a event.
    """

    def __init__(self, uow: IUnitOfWork) -> None:
        self._uow = uow

    async def execute(self, data: EventRetrieveInputDTO) -> EventOutputDTO:
        """
        Executes the use case  by retrieving the event. Returns the retrieved
        event as a EventOutputDTO object.
        :param data:
        :return:
        """

        async with self._uow(autocommit=True):
            event = await self._uow.event.retrieve(event_id=data.event_id)

        return EventOutputDTO.model_validate(event)
