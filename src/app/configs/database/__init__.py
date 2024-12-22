from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncGenerator

from fastapi import FastAPI, Depends
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from app.configs.config import config

Base = declarative_base()

__all__ = (
    'get_async_session',
    'initialize',
)

class SingletonDBManager(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class DataBaseError(Exception):
    pass


@dataclass
class DataBaseManager(metaclass=SingletonDBManager):

    def __init__(self):
        self._engine = None
        self._async_engine = None


    async def __aenter__(self):
        self._async_session = await self.async_session()
        return self._async_session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._async_session.close()

    async def async_engine(self):
        try:
            if self._async_engine is None:
                self._async_engine = create_async_engine(
                    config.DATABASE_URL,
                    future=True,
                    echo=True,
                    pool_size=config.DB_POOL_SIZE,
                    max_overflow=config.DB_MAX_OVERFLOW,
                    pool_recycle=config.DB_POOL_RECYCLE,
                    pool_timeout=10,
                    pool_pre_ping=True,
                )
            return self._async_engine
        except Exception as e:
            raise DataBaseError(f"Error creating async engine: {e}") from e

    async def async_session(self):
        return scoped_session(sessionmaker(bind=await self.async_engine(),
                                           class_=AsyncSession,
                                           expire_on_commit=False,
                                           autoflush=False, autocommit=False))()


db_manager = DataBaseManager()


@asynccontextmanager
async def get_async_session():
    db = await db_manager.async_session()
    try:
        yield db
    finally:
        await db.close()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with get_async_session() as db:
        yield db

async def initialize_async(app: FastAPI, ctx: dict):
    sql_client = db_manager
    try:
        await sql_client.async_engine()
    except Exception as e:
        raise DataBaseError(f"Error initializing database: {e}")
    else:
        ctx["sql_client"] = sql_client
