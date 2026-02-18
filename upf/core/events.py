from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import time
import uuid
from upf.core.event_types import EventType

class BaseEvent(BaseModel):
    event_id: str
    correlation_id: Optional[str]
    event_type: EventType
    timestamp: float
    source_id: str
    payload: Any
    meta: Dict[str, Any] = Field(default_factory=dict)
    processing_history: List[str] = Field(default_factory=list)

    @staticmethod
    def create(event_type: EventType, source_id, payload, correlation_id=None):
        return BaseEvent(
            event_id=str(uuid.uuid4()),
            correlation_id=correlation_id,
            event_type=event_type,
            timestamp=time.time(),
            source_id=source_id,
            payload=payload,
            meta={},
            processing_history=[]
        )
    