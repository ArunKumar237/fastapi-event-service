import asyncio
from datetime import datetime

from sqlalchemy import select

from app.core.logging import logger
from app.db.session import async_session
from app.db.models import Event


async def process_event(event_id: int) -> None:
    """
    Background task for async event processing.
    - Loads event from DB
    - Simulates processing
    - Persists processing result
    """

    async with async_session() as session:
        try:
            result = await session.execute(
                select(Event).where(Event.id == event_id)
            )
            event = result.scalar_one_or_none()

            if event is None:
                logger.error(
                    "Background processing failed: event not found",
                    extra={"event_id": event_id},
                )
                return

            # Simulated async processing (non-blocking)
            await asyncio.sleep(0.1)

            event.processing_status = "processed"
            event.processed_at = datetime.utcnow()
            event.error_message = None

            await session.commit()

            logger.info(
                "Event processed successfully",
                extra={"event_id": event_id},
            )

        except Exception as exc:
            await session.rollback()

            logger.exception(
                "Event processing failed",
                extra={"event_id": event_id},
            )

            # Best-effort failure persistence
            try:
                result = await session.execute(
                    select(Event).where(Event.id == event_id)
                )
                event = result.scalar_one_or_none()
                if event:
                    event.processing_status = "failed"
                    event.error_message = str(exc)
                    await session.commit()
            except Exception:
                logger.exception(
                    "Failed to persist processing failure state",
                    extra={"event_id": event_id},
                )
