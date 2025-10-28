from redis.asyncio import Redis

from src.core.app import redis_client


def cached(
        ttl: int = 300,
        cache: Redis = redis_client,
        key_prefix: str = "cache"):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Генерируем ключ кэша на основе функции и аргументов
            cache_key = f"{key_prefix}:{func.__name__}:{str(args)}:{str(kwargs)}"

            # Пытаемся получить данные из кэша
            cached_result = await cache.get(cache_key)
            if cached_result is not None:
                return cached_result

            # Если в кэше нет, выполняем функцию
            result = await func(*args, **kwargs)

            # Сохраняем результат в кэш
            await cache.set(cache_key, result, ttl)

            return result

        return wrapper

    return decorator
