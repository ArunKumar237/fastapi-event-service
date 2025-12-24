import json
from typing import Any, Dict, List
from sqlalchemy import func, select

from app.cache.redis import redis_client
from app.db.models import Event
from app.db.session import async_session
from app.core.logging import get_logger

logger = get_logger(__name__)


CACHE_KEY = "metrics:events"
CACHE_TTL_SECONDS = 60


async def get_event_metrics() -> List[Dict[str, Any]]:
    """
    Returns aggregated event metrics.
    Uses Redis cache for read optimization.
    """

    cached = await redis_client.get(CACHE_KEY)
    if cached:
        logger.debug("Metrics cache hit", extra={"cache_key": CACHE_KEY})
        return json.loads(cached)

    async with async_session() as session:
        result = await session.execute(
            select(
                Event.event_type,
                Event.source,
                func.count(Event.id).label("count"),
            ).group_by(Event.event_type, Event.source)
        )

        rows = result.all()

        data = [
            {
                "event_type": row.event_type,
                "source": row.source,
                "count": row.count,
            }
            for row in rows
        ]

        await redis_client.set(
            CACHE_KEY,
            json.dumps(data),
            ex=CACHE_TTL_SECONDS,
        )

        return data
