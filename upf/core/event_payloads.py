from pydantic import BaseModel
from typing import Optional, Dict, Any

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