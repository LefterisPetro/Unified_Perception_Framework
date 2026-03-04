from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class MeasurementPayload(BaseModel):
    value: float

class SystemHealthPayload(BaseModel):
    status: str

class AlertPayload(BaseModel):
    message: str
    count: int

class ScoredAlertPayload(BaseModel):
    original_alert: AlertPayload
    confidence: float
    severity: str

class FusionReadyPayload(BaseModel):
    original_alert: ScoredAlertPayload
    confidence: float
    severity: str

class CorrelatedAlertPayload(BaseModel):
    message: str
    original_alert: FusionReadyPayload

class MetricsSnapshotPayload(BaseModel):
    events_total: int
    per_type: Dict[str, int]
    per_source: Dict[str, int]
    started_at: float
    window_seconds: float

class BBoxPayload(BaseModel):
    x: float
    y: float
    w: float
    h: float

class DetectionPayload(BaseModel):
    label: str   # "fire", "smoke", "drone"
    confidence: float  # 0..1
    bbox: Optional[BBoxPayload] = None
    camera_id: Optional[str] = None