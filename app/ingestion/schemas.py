from pydantic import BaseModel, Field
from typing import Dict, Any


class EventIngestRequest(BaseModel):
    event_type: str = Field(..., min_length=1)
    source: str = Field(..., min_length=1)
    payload: Dict[str, Any]


class EventIngestResponse(BaseModel):
    event_id: str
    status: str
