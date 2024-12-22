from abc import ABC, abstractmethod

from app.app_layer.interfaces.clients.bets.dto import EventInputDTO


class IBetClient(ABC):
    @abstractmethod
    async def update_bet(self, data: EventInputDTO) -> None:
        ...
