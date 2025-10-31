from redis.asyncio import ConnectionPool, Redis
import pickle
from typing import Any, Optional

from src.core.settings import settings


class RedisCache:
    def __init__(self):
        self.redis: Optional[Redis] = None

    async def init_redis(self):
        """Инициализация подключения к Redis"""
        self.redis = Redis(
            connection_pool=ConnectionPool(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=1,
            ),
        )

    async def close(self):
        """Закрытие подключения"""
        if self.redis:
            await self.redis.close()

    async def set(self, key: str, value: Any, expire: int = 3600):
        """Сохранение значения в кэш"""
        if self.redis:
            # Сериализуем данные в bytes
            serialized_value = pickle.dumps(value)
            await self.redis.set(key, serialized_value, ex=expire)

    async def get(self, key: str) -> Optional[Any]:
        """Получение значения из кэша"""
        if self.redis:
            data = await self.redis.get(key)
            if data:
                return pickle.loads(data)
        return None

    async def delete(self, key: str):
        """Удаление ключа из кэша"""
        if self.redis:
            await self.redis.delete(key)

    async def exists(self, key: str) -> bool:
        """Проверка существования ключа"""
        if self.redis:
            return await self.redis.exists(key)
        return False
