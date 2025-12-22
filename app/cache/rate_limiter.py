from fastapi import Request, HTTPException

from app.cache.redis import redis_client


async def rate_limiter(request: Request) -> None:
    """
    Minimal Redis-backed rate limiter placeholder.
    Phase 6 will refine limits and strategy.
    """
    client_ip = request.client.host
    key = f"rate:{client_ip}"

    current = await redis_client.incr(key)
    if current == 1:
        await redis_client.expire(key, 60)

    if current > 100:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
