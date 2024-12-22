from app.app_layer.interfaces.unit_of_work.sql import IUnitOfWork
from app.app_layer.use_cases.event.dto import EventListOutputDTO


class EventListUseCase:
    """
    Responsible for retrieving a list of carts based on certain criteria. It uses an
    instance of the IUnitOfWork interface to interact with the data storage and the
    IAuthSystem interface to validate the authentication data.
    """

    def __init__(self, uow: IUnitOfWork) -> None:
        self._uow = uow

    async def execute(self) -> EventListOutputDTO:
        """
        """

        async with self._uow(autocommit=True):
            events = await self._uow.event.get_list(
            )
        return EventListOutputDTO.validate_python(events)