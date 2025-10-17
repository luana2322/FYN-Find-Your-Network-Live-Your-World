from typing import Optional
import redis.asyncio as redis
from .settings import get_settings

_redis: Optional[redis.Redis] = None


async def init_redis() -> None:
    global _redis
    settings = get_settings()
    _redis = redis.from_url(settings.redis_url, decode_responses=True)


async def shutdown_redis() -> None:
    global _redis
    if _redis is not None:
        await _redis.close()
        _redis = None


def get_redis() -> redis.Redis:
    if _redis is None:
        raise RuntimeError("Redis not initialized")
    return _redis
