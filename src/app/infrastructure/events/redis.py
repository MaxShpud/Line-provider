import asyncio
import json
from datetime import datetime
from typing import Any, Union
from uuid import UUID
import pickle

from arq import ArqRedis
from arq.connections import RedisSettings, create_pool
from redis.asyncio import Redis, RedisError

from app.config import Config


config = Config()

class RedisService:
    def __init__(self, redis_client: Redis) -> None:
        self._redis = redis_client

    async def put_data(self, key: str, data: Any, deadline: Union[datetime, None]) -> None:
        try:
            if deadline < datetime.now():
                await self._redis.delete(key)
            else:
                await self._redis.set(key, pickle.dumps(data))
                await self._redis.expireat(key, deadline)
        except (ConnectionError, OSError, RedisError, asyncio.TimeoutError) as err:
            raise

    async def get_data(self, key: str) -> Any:
        try:
            data = await self._redis.get(key)
            if data:
                return pickle.loads(data)
            return None
        except (ConnectionError, OSError, RedisError, asyncio.TimeoutError) as err:
            raise


async def init_arq_task_broker(config: Config) -> ArqRedis:
    """ """
    redis_settings = RedisSettings(host=config.host, port=config.port, password=config.password)
    pool = await create_pool(redis_settings)
    return pool
