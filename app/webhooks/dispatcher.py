import asyncio
from typing import Dict
from sqlalchemy import select
from app.db.session import async_session
from app.db.models import Event
from app.webhooks.service import get_webhooks_for_event

from app.core.logging import get_logger

logger = get_logger(__name__)


# In-memory delivery attempts
_DELIVERY_ATTEMPTS: Dict[str, int] = {}

MAX_RETRIES = 3
BASE_DELAY = 0.5  # seconds


async def dispatch_webhook(event_id: str) -> None:
    async with async_session() as session:
        result = await session.execute(
            select(Event).where(Event.id == event_id)
        )
        event = result.scalar_one_or_none()

        if not event:
            logger.error(
                "Webhook dispatch failed: event not found",
                extra={"event_id": event_id},
            )
            return

        webhooks = get_webhooks_for_event(event.event_type)

        for url in webhooks:
            await _deliver_with_retry(event, url)


async def _deliver_with_retry(event: Event, url: str) -> None:
    key = f"{event.id}:{url}"

    attempts = _DELIVERY_ATTEMPTS.get(key, 0)

    while attempts < MAX_RETRIES:
        try:
            # Simulated async HTTP call
            await asyncio.sleep(0.1)

            logger.info(
                "Webhook delivered",
                extra={
                    "event_id": event.id,
                    "target_url": url,
                    "attempt": attempts + 1,
                },
            )

            _DELIVERY_ATTEMPTS.pop(key, None)
            return

        except Exception:
            attempts += 1
            _DELIVERY_ATTEMPTS[key] = attempts

            delay = BASE_DELAY * (2 ** (attempts - 1))
            logger.warning(
                "Webhook delivery attempt failed, will retry",
                extra={
                    "event_id": event.id,
                    "target_url": url,
                    "attempt": attempts,
                    "delay": delay,
                },
                exc_info=True,
            )

            await asyncio.sleep(delay)

    logger.error(
        "Webhook delivery permanently failed",
        extra={"event_id": event.id, "target_url": url, "attempts": attempts},
    )
