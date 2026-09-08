import redis
import json
import os
import hashlib

redis_client = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))

async def get_cache(query: str) -> str | None:
    """استرجاع النتائج من الكاش"""
    key = hashlib.sha256(query.encode()).hexdigest()
    cached = redis_client.get(key)
    if cached:
        return cached.decode('utf-8')
    return None

async def set_cache(query: str, data: str, ttl: int = 600) -> None:
    """تخزين النتائج في الكاش لمدة 10 دقائق"""
    key = hashlib.sha256(query.encode()).hexdigest()
    redis_client.setex(key, ttl, data)