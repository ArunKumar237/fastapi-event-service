from typing import Dict, List

from app.core.logging import logger

# In-memory registry (Phase 4 only)
_WEBHOOK_REGISTRY: Dict[str, List[str]] = {}


def register_webhook(event_type: str, target_url: str) -> None:
    urls = _WEBHOOK_REGISTRY.setdefault(event_type, [])
    urls.append(target_url)

    logger.info(
        "Webhook registered",
        extra={"event_type": event_type, "target_url": target_url},
    )


def get_webhooks_for_event(event_type: str) -> List[str]:
    return _WEBHOOK_REGISTRY.get(event_type, [])
