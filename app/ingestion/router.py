from fastapi import APIRouter, Depends, BackgroundTasks

from app.ingestion.schemas import EventIngestRequest, EventIngestResponse
from app.ingestion.service import ingest_event
from app.db.session import async_session
from app.cache.rate_limiter import rate_limiter
from app.core.logging import logger

router = APIRouter(prefix="/events", tags=["events"])


@router.post(
    "",
    response_model=EventIngestResponse,
    dependencies=[Depends(rate_limiter)],
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

    # Phase 3 will attach real processing logic here
    background_tasks.add_task(
        logger.info,
        "background_task_scheduled",
        event_id=event_id,
    )

    return EventIngestResponse(
        event_id=event_id,
        status="accepted",
    )
