from fastapi import APIRouter, BackgroundTasks, status
from pydantic import BaseModel, HttpUrl
from app.webhooks.service import register_webhook
from app.webhooks.dispatcher import dispatch_webhook

from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/webhooks", tags=["webhooks"])



class WebhookRegisterRequest(BaseModel):
    event_type: str
    target_url: HttpUrl


@router.post("", status_code=status.HTTP_201_CREATED)
async def register_webhook_endpoint(
    payload: WebhookRegisterRequest,
):
    register_webhook(payload.event_type, str(payload.target_url))
    return {"status": "registered"}


@router.post("/dispatch/{event_id}")
async def dispatch_webhook_endpoint(
    event_id: str,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(dispatch_webhook, event_id)
    logger.info("Webhook dispatch scheduled", extra={"event_id": event_id})
    return {"status": "dispatch_started"}
