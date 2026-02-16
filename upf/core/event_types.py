from enum import Enum

class EventType(str, Enum):
    MEASUREMENT = "MeasurementEvent"
    ALERT = "AlertEvent"
    SYSTEM_HEALTH = "SystemHealthEvent"
    CORRELATED_ALERT = "CorrelatedAlertEvent"