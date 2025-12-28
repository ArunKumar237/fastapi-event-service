from fastapi import Request, HTTPException

from app.cache.redis import redis_client
from app.core.logging import get_logger

logger = get_logger(__name__)



async def rate_limiter(request: Request) -> None:
    """
    Minimal Redis-backed rate limiter placeholder.
    Phase 6 will refine limits and strategy.
    """
    client_ip = request.client.host
    key = f"rate:{client_ip}"

    try:
        current = await redis_client.incr(key)
        if current == 1:
            await redis_client.expire(key, 60)
    except Exception:
        # Fail-open: allow requests if Redis is unavailable but log the incident
        logger.exception("Rate limiter Redis error", extra={"client_ip": client_ip, "key": key})
        return

    if current > 100:
        logger.warning(
            "Rate limit exceeded",
            extra={"client_ip": client_ip, "key": key, "count": current, "request_id": getattr(request.state, "request_id", None)},
        )
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
