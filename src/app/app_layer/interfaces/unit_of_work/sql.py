from abc import ABC, abstractmethod
from typing import Union

from app.domain.interfaces.repositories.event.repo import IEventRepository


class IUnitOfWork(ABC):
    event: IEventRepository

    def __call__(self, autocommit: bool, *args, **kwargs) -> "IUnitOfWork":
        self._autocommit = autocommit
        return self

    async def __aenter__(self) -> "IUnitOfWork":
        return self

    async def __aexit__(
        self, exc_type: Union[type[BaseException], None], *args, **kwargs
    ) -> None:
        if exc_type is not None:
            await self.rollback()
        else:
            if self._autocommit:
                await self.commit()

        await self.shutdown()

    @abstractmethod
    async def commit(self) -> None:
        ...

    @abstractmethod
    async def rollback(self) -> None:
        ...

    @abstractmethod
    async def shutdown(self) -> None:
        ...
