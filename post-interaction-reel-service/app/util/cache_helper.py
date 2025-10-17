import json
import redis
from typing import List, Optional, Any
from app.config.redis_config import get_redis
from app.config.settings import settings

class CacheHelper:
    def __init__(self):
        self.redis_client = get_redis()
        self.default_ttl = settings.CACHE_TTL
    
    def set_cache(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set cache value with TTL"""
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            ttl = ttl or self.default_ttl
            self.redis_client.setex(key, ttl, value)
            return True
        except Exception as e:
            print(f"Cache set error: {e}")
            return False
    
    def get_cache(self, key: str) -> Optional[Any]:
        """Get cache value"""
        try:
            value = self.redis_client.get(key)
            if value:
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value
            return None
        except Exception as e:
            print(f"Cache get error: {e}")
            return None
    
    def delete_cache(self, key: str) -> bool:
        """Delete cache key"""
        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            print(f"Cache delete error: {e}")
            return False
    
    def delete_pattern(self, pattern: str) -> int:
        """Delete all keys matching pattern"""
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                return self.redis_client.delete(*keys)
            return 0
        except Exception as e:
            print(f"Cache pattern delete error: {e}")
            return 0
    
    def cache_user_feed(self, user_id: int, posts: List[dict], ttl: Optional[int] = None) -> bool:
        """Cache user's personalized feed"""
        key = f"user_feed:{user_id}"
        return self.set_cache(key, posts, ttl)
    
    def get_user_feed(self, user_id: int) -> Optional[List[dict]]:
        """Get user's cached feed"""
        key = f"user_feed:{user_id}"
        return self.get_cache(key)
    
    def cache_global_feed(self, posts: List[dict], ttl: Optional[int] = None) -> bool:
        """Cache global feed"""
        key = "global_feed"
        return self.set_cache(key, posts, ttl)
    
    def get_global_feed(self) -> Optional[List[dict]]:
        """Get cached global feed"""
        key = "global_feed"
        return self.get_cache(key)
    
    def cache_reel_feed(self, reels: List[dict], ttl: Optional[int] = None) -> bool:
        """Cache reel feed"""
        key = "reel_feed"
        return self.set_cache(key, reels, ttl)
    
    def get_reel_feed(self) -> Optional[List[dict]]:
        """Get cached reel feed"""
        key = "reel_feed"
        return self.get_cache(key)
    
    def invalidate_user_feed(self, user_id: int) -> bool:
        """Invalidate user's feed cache"""
        key = f"user_feed:{user_id}"
        return self.delete_cache(key)
    
    def invalidate_global_feed(self) -> bool:
        """Invalidate global feed cache"""
        key = "global_feed"
        return self.delete_cache(key)
    
    def invalidate_reel_feed(self) -> bool:
        """Invalidate reel feed cache"""
        key = "reel_feed"
        return self.delete_cache(key)
    
    def cache_post_stats(self, post_id: int, stats: dict, ttl: Optional[int] = None) -> bool:
        """Cache post statistics"""
        key = f"post_stats:{post_id}"
        return self.set_cache(key, stats, ttl)
    
    def get_post_stats(self, post_id: int) -> Optional[dict]:
        """Get cached post statistics"""
        key = f"post_stats:{post_id}"
        return self.get_cache(key)
    
    def cache_reel_stats(self, reel_id: int, stats: dict, ttl: Optional[int] = None) -> bool:
        """Cache reel statistics"""
        key = f"reel_stats:{reel_id}"
        return self.set_cache(key, stats, ttl)
    
    def get_reel_stats(self, reel_id: int) -> Optional[dict]:
        """Get cached reel statistics"""
        key = f"reel_stats:{reel_id}"
        return self.get_cache(key)
    
    def increment_like_count(self, post_id: int) -> int:
        """Increment like count in cache"""
        key = f"post_likes:{post_id}"
        try:
            return self.redis_client.incr(key)
        except Exception as e:
            print(f"Cache increment error: {e}")
            return 0
    
    def decrement_like_count(self, post_id: int) -> int:
        """Decrement like count in cache"""
        key = f"post_likes:{post_id}"
        try:
            return self.redis_client.decr(key)
        except Exception as e:
            print(f"Cache decrement error: {e}")
            return 0
    
    def get_like_count(self, post_id: int) -> int:
        """Get like count from cache"""
        key = f"post_likes:{post_id}"
        try:
            count = self.redis_client.get(key)
            return int(count) if count else 0
        except Exception as e:
            print(f"Cache get count error: {e}")
            return 0

