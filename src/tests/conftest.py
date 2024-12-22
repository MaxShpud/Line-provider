import asyncio
from asyncio import AbstractEventLoop
from decimal import Decimal

import pytest
from _pytest.fixtures import SubRequest
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import Config, DBConfig
from app.infrastructure.repositories.sqla.db import Database


@pytest.fixture(scope='session')
def config() -> Config:
    return Config()

@pytest.fixture(scope='session')
async def db_config(event_loop: AbstractEventLoop, config: Config) -> DBConfig:
    return config.DB.model_copy(update={"dsn": str(config.DB.dsn) + "_test"})

@pytest.fixture(scope="session")
async def sqla_database(db_config: DBConfig, database: None) -> Database:
    return Database(db_config)


@pytest.fixture(scope="session")
async def sqla_engine(sqla_database: Database) -> AsyncEngine:
    yield sqla_database.engine
    await sqla_database.engine.dispose()


@pytest.fixture()
async def session_factory(
    sqla_engine: AsyncEngine,
    sqla_database: Database,
) -> async_sessionmaker[AsyncSession]:
    """
    Fixture that returns a SQLAlchemy sessionmaker with a SAVEPOINT, and the rollback to it
    after the test completes.
    """

    connection = await sqla_engine.connect()
    trans = await connection.begin()

    yield async_sessionmaker(
        bind=connection,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )

    await trans.rollback()
    await connection.close()
