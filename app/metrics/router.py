from app.cache.rate_limiter import rate_limiter
from app.core.security import api_key_auth
from fastapi import APIRouter, Depends

from app.metrics.service import get_event_metrics

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/events", dependencies=[Depends(api_key_auth), Depends(rate_limiter)])
async def metrics_events():
    return await get_event_metrics()
