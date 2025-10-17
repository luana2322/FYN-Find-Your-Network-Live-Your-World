from typing import Optional
from redis.asyncio import Redis


class PresenceRepository:
    def __init__(self, redis_client: Redis) -> None:
        self.redis = redis_client
        self.key_prefix = "presence:user:"

    def _key(self, user_id: str) -> str:
        return f"{self.key_prefix}{user_id}"

    async def set_online(self, user_id: str, connection_id: str, ttl_seconds: int = 60) -> None:
        key = self._key(user_id)
        await self.redis.set(key, connection_id, ex=ttl_seconds)

    async def set_offline(self, user_id: str) -> None:
        await self.redis.delete(self._key(user_id))

    async def is_online(self, user_id: str) -> bool:
        return await self.redis.exists(self._key(user_id)) == 1

    async def get_connection(self, user_id: str) -> Optional[str]:
        value = await self.redis.get(self._key(user_id))
        return value if value is not None else None
