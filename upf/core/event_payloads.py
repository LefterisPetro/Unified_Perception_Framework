from pydantic import BaseModel
from typing import Optional, Dict, Any, List, Union

class MeasurementPayload(BaseModel):
    value: float 

class SystemHealthPayload(BaseModel):
    status: str # e.g. "ok", "degraded", "critical"

class AlertPayload(BaseModel):
    message: str # a human-readable message describing the alert
    count: int # number of times this alert has been observed within the time window

class ScoredAlertPayload(BaseModel):
    original_alert: Union[VisionAlertPayload, AlertPayload] # the original alert that was scored, can be a VisionAlert or a generic Alert
    confidence: float # confidence that this alert is a true positive, 0..1
    severity: str # severity level of the alert, e.g. "low", "medium", "high"

class FusionReadyPayload(BaseModel):
    original_alert: ScoredAlertPayload # the original alert that was scored and is now ready for fusion
    confidence: float # confidence that this alert is a true positive and should be fused, 0..1
    severity: str # severity level of the alert, e.g. "low", "medium", "high"

class CorrelatedAlertPayload(BaseModel):
    message: str # a summary message for the correlated alert
    original_alert: FusionReadyPayload # the original alert that was fused and scored

class MetricsSnapshotPayload(BaseModel):
    events_total: int # total number of events received in this snapshot
    per_type: Dict[str, int] # count of events per type
    per_source: Dict[str, int] # count of events per source
    started_at: float # timestamp when the snapshot was started
    window_seconds: float # duration of the snapshot window in seconds

class BBoxPayload(BaseModel):
    x: float # normalized x coordinate of the top-left corner of the bounding box (0..1)
    y: float # normalized y coordinate of the top-left corner of the bounding box (0..1)
    w: float # normalized width of the bounding box (0..1)
    h: float # normalized height of the bounding box (0..1)

class DetectionPayload(BaseModel):
    label: str   # "fire", "smoke", "drone"
    confidence: float  # 0..1
    bbox: Optional[BBoxPayload] = None # bounding box of the detection in the image, if available (x,y,w,h) normalized to [0..1]
    camera_id: Optional[str] = None # identifier for the camera that generated this detection

class VisionAlertPayload(BaseModel):
    label: str   # "fire", "smoke", "drone"
    hits: int # number of detections that contributed to this alert within the time window
    window_seconds: float # how long the detections were observed in seconds
    min_confidence: float # minimum confidence of the detections that led to this alert
    max_confidence: float # maximum confidence of the detections that led to this alert
    camera_id: Optional[str] = None # identifier for the camera that generated this alert

class RFCuePayload(BaseModel):
    band_hz: float # e.g. 2.4e9 for 2.4 GHz band or 5.8e9 for 5.8 GHz band
    center_freq_hz: float # e.g. 2.437e9 
    bandwidth_hz: float # e.g. 2.0e6 
    snr_db: float # signal-to-noise ratio in decibels (quick quality indicator for the cue)
    confidence: float # 0..1 (your RF detector output)
    sensor_id: str = "hackrf" # identifier for the RF sensor that generated this cue
    note: Optional[str] = None # any additional notes or metadata about this RF cue
