import time
from collections import deque, defaultdict

from upf.core.events import BaseEvent
from upf.core.event_types import EventType
from upf.core.event_payloads import AlertPayload

class VisionTemporalProcessor:
    @property
    
    def supported_event_types(self):
        return [EventType.DETECTION]
    
    def __init__(
            self,
            window_seconds: float = 3.0,
            drone_min_confidence: float = 0.65,
            drone_min_count: int = 2,
            fire_min_confidence: float = 0.80
    ):
        self.window_seconds = window_seconds
        self.drone_min_confidence = drone_min_confidence
        self.drone_min_count = drone_min_count
        self.fire_min_confidence = fire_min_confidence

        self.events = deque()  # Store recent events for temporal analysis
        self.active = defaultdict(bool) # Track active alerts to prevent duplicates

    async def process(self, event, bus):
        now = time.time()
        det = event.payload # Assuming payload is a DetectionPayload

        self.events.append((now, det.label, det.confidence)) # Store timestamp, label, and confidence

        while self.events and (now - self.events[0][0] > self.window_seconds):
            self.events.popleft() # Remove old events outside the window

        if det.label == "fire": #FIRE rule: if a fire detection with confidence above threshold is seen, trigger alert immediately
            if det.confidence >= self.fire_min_confidence and not self.active["fire"]: # If confidence meets threshold and we haven't already triggered a fire alert, publish an alert and set active state
                self.active["fire"] = True

                alert_payload = AlertPayload(
                    message=f"Vision: FIRE detected (conf={det.confidence})",
                    count=1
                )
                alert = BaseEvent.create(
                    event_type=EventType.ALERT,
                    source_id="vision_temporal_processor",
                    payload=alert_payload,
                    correlation_id=event.event_id
                )
                await bus.publish(alert)
            return
        
        if det.label == "drone":
            hits = sum(1 for _, label, conf in self.events if label == "drone" and conf >= self.drone_min_confidence) # Count recent drone detections above confidence threshold

            if hits >= self.drone_min_count and not self.active["drone"]: # If the count meets the threshold and we haven't already triggered an alert, publish an alert and set active state
                self.active["drone"] = True

                alert_payload = AlertPayload(
                    message=f"Vision: DRONE detected (hits={hits}, in {self.window_seconds} seconds)",
                    count=hits
                )
                alert = BaseEvent.create(
                    event_type=EventType.ALERT,
                    source_id="vision_temporal_processor",
                    payload=alert_payload,
                    correlation_id=event.event_id
                )
                await bus.publish(alert)

            if hits < self.drone_min_count: # If the count falls below the threshold, reset the active state to allow future alerts
                self.active["drone"] = False
                