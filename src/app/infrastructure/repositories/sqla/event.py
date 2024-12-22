from uuid import UUID

from sqlalchemy import select, Row
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update


from app.domain.event.dto import EventDTO
from app.domain.event.entity import Event
from app.domain.event.value_objects import EventStatusEnum
from app.domain.interfaces.repositories.event.exceptions import ActiveEventAlreadyExistsError, EventNotFoundError, \
    EventUpdateError
from app.domain.interfaces.repositories.event.repo import IEventRepository
from app.infrastructure.repositories.sqla import models


class EventRepository(IEventRepository):
    """
    Responsible for interacting with the database to perform CRUD operations on the
    Event objects. It provides methods to create a new event, retrieve an existing
    event, update a event's status and etc.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, event: Event) -> Event:
        """
        Creates a new event in the database and returns the created cart object.
        """
        stmt = insert(models.Event).values(
            id=event.id,
            coefficient=event.coefficient,
            created_at=event.created_at,
            deadline=event.deadline,
            status=event.status,
            type=event.type,
            info=event.info,
        )

        try:
            await self._session.execute(stmt)
        except IntegrityError:
           raise ActiveEventAlreadyExistsError

        return event

    async def retrieve(self, event_id: UUID) -> Event:
        """
        Retrieve an existing event from the database.
        """
        stmt = (select(
            models.Event)
                .where(
                    models.Event.id == event_id
                )
        )
        result = await self._session.scalars(stmt)
        obj = result.first()

        if not obj:
            raise EventNotFoundError

        event = self._get_event(obj)
        return event



    async def update(self, event: Event) -> Event:
        """
        Updates an existing event in the database.
        """
        stmt = (
            update(models.Event)
            .where(models.Event.id == event.id)
            .values(
                coefficient=event.coefficient,
                deadline=event.deadline,
                status=event.status,
                type=event.type,
                info=event.info,
                updated_at=event.updated_at,
            )
        )
        try:
            await self._session.execute(stmt)
        except SQLAlchemyError:
            raise EventUpdateError
        return event

    async def get_list(self) -> list[Event]:
        """
        Retrieves a list of events from the database and returns a list of event objects.
        """

        stmt = (
            select(models.Event)
            .order_by(models.Event.created_at.desc())
        )
        result = await self._session.scalars(stmt)
        objects = result.unique().all()


        return [self._get_event(obj=obj) for obj in objects]

    @staticmethod
    def _get_event(obj: Row):
        event = Event(
            data=EventDTO.model_validate(obj)
        )
        return event
