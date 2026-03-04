import time
from collections import deque, defaultdict

from upf.core.events import BaseEvent
from upf.core.event_types import EventType
from upf.core.event_payloads import AlertPayload

class VisionTemporalProcessor:
    @property
    
    def supported_event_types(self):
        return [EventType.DETECTION]
    
    def __init__(self, rules: dict):
        """
        rules example:
        {
          "fire":  {"window_seconds":3, "min_confidence":0.8, "min_count":1},
          "smoke": {"window_seconds":5, "min_confidence":0.6, "min_count":2},
          "drone": {"window_seconds":3, "min_confidence":0.65,"min_count":2},
        }
        """
        self.rules = rules
        self.events_by_label = defaultdict(deque)  # label -> deque of (timestamp, confidence)
        self.active = defaultdict(bool)  # label -> whether an alert is currently active for that label

    async def process(self, event, bus):
        det = event.payload
        label = det.label  # Assuming payload is a DetectionPayload

        rule = self.rules.get(label)
        if not rule:
            return # No rule for this label, ignore 
        
        window_seconds = float(rule["window_seconds"])
        min_confidence = float(rule["min_confidence"])
        min_count = int(rule["min_count"])
        now = time.time()

        if det.confidence >= min_confidence: # Only consider detections that meet the confidence threshold
            self.events_by_label[label].append((now, det.confidence))

        # Remove old events outside the time window
        q = self.events_by_label[label]
        while q and (now - q[0][0] > window_seconds):
            q.popleft()

        hits = len(q)

        if hits >= min_count and not self.active[label]:   # Only trigger alert if we have enough hits and no active alert for this label
            self.active[label] = True

            alert_payload = AlertPayload(
                message=f"Vision: {label.upper()} detected (hits={hits} in {window_seconds}s)",
                count=hits
            )

            alert = BaseEvent.create(
                event_type=EventType.ALERT,
                source_id="vision_temporal_processor",
                payload=alert_payload,
                correlation_id=event.event_id
            )
            await bus.publish(alert)

        if hits < min_count:   # If we no longer meet the criteria for an active alert, reset the active state
            self.active[label] = False  