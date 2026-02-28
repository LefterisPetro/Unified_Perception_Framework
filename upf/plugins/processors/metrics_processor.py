import time
from collections import defaultdict
from upf.core.events import BaseEvent
from upf.core.event_types import EventType
from upf.core.event_payloads import MetricsSnapshotPayload

class MetricsProcessor:
    @property
    def supported_event_types(self): #τραβάει όλα τα EventType values προς το παρών
        return list(EventType)
    
    def __init__(self, window_seconds: float = 5.0, source_id="metrics"):
        self.window_seconds = window_seconds
        self.source_id = source_id
        self.started_at = time.time()
        self.last_emit = self.started_at
        self.events_total = 0
        self.per_type = defaultdict(int)
        self.per_source = defaultdict(int)

    async def process(self, event, bus):
        if event.event_type == EventType.METRICS_SNAPSHOT:
            return
        
        self.events_total += 1
        self.per_type[event.event_type.value] += 1
        self.per_source[event.source_id] += 1

        now = time.time()

        if now - self.last_emit >= self.window_seconds:
            payload = MetricsSnapshotPayload(
                events_total=self.events_total,
                per_type=dict(self.per_type),
                per_source=dict(self.per_source),
                started_at=self.started_at,
                window_seconds=self.window_seconds
            )
            snapshot = BaseEvent.create(
                event_type=EventType.METRICS_SNAPSHOT,
                source_id=self.source_id,
                payload=payload
            )
            self.last_emit = now
            await bus.publish(snapshot)