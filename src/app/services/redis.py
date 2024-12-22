import pickle
from typing import Any, List

from app.configs.config import config
from app.configs.redis import cache


class RedisService:
    @staticmethod
    async def get_all_data() -> List[Any]:
        """Retrieve all data from Redis."""
        all_data = []
        try:
            for key in cache.scan_iter("*"):
                data = cache.get(key)
                if data:
                    all_data.append(pickle.loads(data))
        except Exception as err:
            raise RuntimeError(f"Failed to retrieve data: {err}")
        return all_data

    @staticmethod
    def get_data_by_key(key: str) -> Any:
        cached = cache.get(key)
        if not cached:
            return
        return pickle.loads(cached)

    @staticmethod
    def put_data(key: str, data: Any) -> None:
        cache.set(key, pickle.dumps(data), ex=config.REDIS_CACHING_TIME)
