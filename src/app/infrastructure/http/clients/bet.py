
from typing import Any

from pydantic import AnyHttpUrl
from furl import furl

from app.app_layer.interfaces.clients.bets.bet import IBetClient
from app.app_layer.interfaces.clients.bets.dto import EventInputDTO
from app.app_layer.interfaces.clients.bets.exceptions import BetsClientError
from app.domain.event.value_objects import EventStatusEnum
from app.infrastructure.http.transports.base import IHttpTransport, HttpRequestInputDTO, HttpTransportError, HTTPMethod


class BetHttpClient(IBetClient):
    """
    Responsible for making HTTP requests to updating bet information from a
    remote server.
    """

    def __init__(self, base_url: AnyHttpUrl, transport: IHttpTransport) -> None:
        self._base_url = base_url
        self._transport = transport

    async def update_bet(self, data: EventInputDTO) -> None:
        """
        """

        url = furl(self._base_url).add(path="status").url
        await self._try_to_make_request(
            data=HttpRequestInputDTO(
                method=HTTPMethod.PUT,
                url=url,
                headers={"Accept": "application/json"},
                body={
                    "event_id": str(data.event_id),
                    "status": data.status.value,
                },
            ),
        )

    async def _try_to_make_request(self, *args, **kwargs) -> Any:
        try:
            return await self._transport.request(*args, **kwargs)
        except HttpTransportError as err:
            raise BetsClientError(str(err))