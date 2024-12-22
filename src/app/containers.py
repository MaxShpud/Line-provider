from contextlib import asynccontextmanager
from types import ModuleType
from typing import AsyncContextManager

from dependency_injector import containers, providers

from app.app_layer.use_cases.event.create_event import CreateEventUseCase
from app.app_layer.use_cases.event.event_list import EventListUseCase
from app.app_layer.use_cases.event.retrieve_event import RetrieveEventUseCase
from app.app_layer.use_cases.event.update_event import UpdateEventUseCase
from app.config import Config
from app.infrastructure.events.redis import init_arq_task_broker, RedisService
from app.infrastructure.http.clients.bet import BetHttpClient
from app.infrastructure.http.retry_systems.backoff import BackoffRetrySystem, BackoffConfig
from app.infrastructure.http.transports.aiohttp import AioHttpTransport, init_aiohttp_session_pool
from app.infrastructure.http.transports.base import RetryableHttpTransport, HttpTransportConfig
from app.infrastructure.repositories.sqla.db import Database
from app.infrastructure.unit_of_work.sqla import Uow


class EventsContainer(containers.DeclarativeContainer):
    config = providers.Dependency(instance_of=Config)
    broker = providers.Resource(init_arq_task_broker, config=config.provided.ARQ_REDIS)
    redis_service = providers.Factory(RedisService, redis_client=broker)


class DBContainer(containers.DeclarativeContainer):
    config = providers.Dependency(instance_of=Config)
    db = providers.Singleton(Database, config=config.provided.DB)
    uow = providers.Factory(Uow, session_factory=db.provided.session_factory)

class BetClientContainer(containers.DeclarativeContainer):
    config = providers.Dependency(instance_of=Config)
    transport = providers.Factory(
        RetryableHttpTransport,
        transport=providers.Factory(
            AioHttpTransport,
            session=providers.Resource(init_aiohttp_session_pool),
            config=providers.Factory(
                HttpTransportConfig,
                integration_name=config.provided.BET_CLIENT.name,
            ),
        ),
        retry_system=providers.Factory(
            BackoffRetrySystem,
            config=providers.Factory(
                BackoffConfig,
                enabled=config.provided.BET_CLIENT.retries_enabled,
            ),
        ),
    )
    client = providers.Factory(
        BetHttpClient,
        base_url=config.provided.BET_CLIENT.base_url,
        transport=transport,
    )

class Container(containers.DeclarativeContainer):
    config = Config()
    events = providers.Container(EventsContainer, config=config)
    db = providers.Container(DBContainer, config=config)
    bet_client = providers.Container(
        BetClientContainer, config=config
    )

    create_event_use_case = providers.Factory(
        CreateEventUseCase,
        uow=db.container.uow,
        redis_service=events.container.redis_service
    )
    retrieve_event_use_case = providers.Factory(
        RetrieveEventUseCase,
        uow=db.container.uow
    )
    update_event_use_case = providers.Factory(
        UpdateEventUseCase,
        uow=db.container.uow,
        redis_service=events.container.redis_service,
        bet_client=bet_client.container.client,
    )
    event_list_use_case = providers.Factory(
        EventListUseCase,
        uow=db.container.uow
    )
    @classmethod
    @asynccontextmanager
    async def lifespan(
            cls, wireable_packages: list[ModuleType]
    ) -> AsyncContextManager["Container"]:
        container = cls()
        container.wire(packages=wireable_packages)

        result = container.init_resources()
        if result:
            await result
        if result:
            await result

        yield container