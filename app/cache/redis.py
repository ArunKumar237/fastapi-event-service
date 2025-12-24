import redis.asyncio as redis
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

redis_client = redis.from_url(settings.redis_url, decode_responses=True)

logger.debug("Redis client initialized")
