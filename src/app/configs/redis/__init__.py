import pickle
from typing import Any, List

from redis import Redis

from app.configs.config import config


cache = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    password=config.REDIS_PASSWORD,
)