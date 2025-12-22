from fastapi import APIRouter

from app.metrics.service import get_event_metrics

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/events")
async def metrics_events():
    return await get_event_metrics()
