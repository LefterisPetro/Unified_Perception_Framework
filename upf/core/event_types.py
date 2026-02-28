from enum import Enum

class EventType(str, Enum):
    MEASUREMENT = "MeasurementEvent"
    ALERT = "AlertEvent"
    SYSTEM_HEALTH = "SystemHealthEvent"
    CORRELATED_ALERT = "CorrelatedAlertEvent"
    SCORED_ALERT = "ScoredAlertEvent"
    FUSION_READY_ALERT = "FusionReadyAlertEvent"
    METRICS_SNAPSHOT = "MetricsSnapshot"
    DETECTION = "Detection"