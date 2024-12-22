from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.event.entity import Event


class IEventRepository(ABC):
    @abstractmethod
    async def create(self, event: Event) -> Event:
        ...

    @abstractmethod
    async def retrieve(self, event_id: UUID) -> Event:
        ...

    @abstractmethod
    async def update(self, event: Event) -> Event:
        ...

    @abstractmethod
    async def get_list(self) -> list[Event]:
        ...