from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Event
from app.utils.ids import generate_event_id
from app.core.logging import get_logger

logger = get_logger(__name__)



async def ingest_event(
    db: AsyncSession,
    event_type: str,
    source: str,
    payload: dict,
) -> str:
    event_id = generate_event_id()

    event = Event(
        id=event_id,
        event_type=event_type,
        source=source,
        payload=payload,
    )

    db.add(event)
    await db.commit()

    logger.info(
        "Event ingested",
        extra={
            "event_id": event_id,
            "event_type": event_type,
            "source": source,
        },
    )

    return event_id
