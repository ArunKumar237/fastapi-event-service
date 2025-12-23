import asyncio
from fastapi import APIRouter, Depends, BackgroundTasks

from app.ingestion.schemas import EventIngestRequest, EventIngestResponse
from app.ingestion.service import ingest_event
from app.background.tasks import process_event
from app.db.session import async_session
from app.cache.rate_limiter import rate_limiter
from app.core.logging import logger
from app.core.security import api_key_auth

router = APIRouter(prefix="/events", tags=["events"])


@router.post(
    "",
    response_model=EventIngestResponse,
    dependencies=[Depends(api_key_auth), Depends(rate_limiter)],
)
async def ingest_event_endpoint(
    request: EventIngestRequest,
    background_tasks: BackgroundTasks,
):
    async with async_session() as db:
        event_id = await ingest_event(
            db=db,
            event_type=request.event_type,
            source=request.source,
            payload=request.payload,
        )

    asyncio.create_task(process_event(event_id))

    logger.info(
        "background_task_scheduled",
        extra={"event_id": event_id},
    )

    return EventIngestResponse(
        event_id=event_id,
        status="accepted",
    )
