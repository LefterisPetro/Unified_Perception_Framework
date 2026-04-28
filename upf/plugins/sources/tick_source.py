import asyncio
from upf.core.events import BaseEvent
from upf.core.event_types import EventType

class TickSource:
    def __init__(self, interval_seconds: float = 1.0, source_id: str = "tick"):
        self.interval_seconds = float(interval_seconds)
        self.source_id = source_id
    
    async def start(self, bus):
        while True:
            evt = BaseEvent.create(
                event_type=EventType.TICK,
                source_id=self.source_id,
                payload={"interval_seconds": self.interval_seconds},
            )
            await bus.publish(evt)
            await asyncio.sleep(self.interval_seconds)