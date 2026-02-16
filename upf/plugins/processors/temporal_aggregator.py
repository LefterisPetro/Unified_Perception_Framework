import time
from collections import deque
from upf.core.events import BaseEvent

class TemporalAggregatorProcessor:

    @property
    def supported_event_types(self):
        return["MeasurementEvent"]
    
    def __init__(self, threshold, window_seconds, min_count):
        self.threshold = threshold
        self.window_seconds = window_seconds
        self.min_count = min_count
        self.events = deque()
        self.active = False

    async def process(self, event, bus):
        
        value = event.payload.get("value")
        if value is None:
            return
        
        now = time.time()

        #Προσθέτουμε event στο window
        self.events.append((now, value))

        #Καθαρίζουμε παλιά events
        while self.events and (now - self.events[0][0] > self.window_seconds):
            self.events.popleft()

        #Μετράμε πόσα είναι πάνω από threshold
        count = sum(1 for _, v in self.events if v > self.threshold)

        if count >= self.min_count and not self.active:
            self.active = True

            alert = BaseEvent.create(
                event_type="AlertEvent",
                source_id="temporal_aggregator",
                payload={
                    "message": "Temporal threshold exceeded",
                    "count": count
                },
                correlation_id=event.event_id
            )

            await bus.publish(alert)
        
        elif count < self.min_count:
            self.active = False
