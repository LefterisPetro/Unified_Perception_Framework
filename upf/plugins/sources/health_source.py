import asyncio
from upf.core.events import BaseEvent
from upf.core.event_types import EventType
from upf.core.event_payloads import SystemHealthPayload

class HealthSource:
    
    def __init__(self, source_id="system_health"):
        self.source_id = source_id

    async def start(self, bus):
        while True:

            health_payload = SystemHealthPayload(status="OK")

            event = BaseEvent.create(
                event_type=EventType.SYSTEM_HEALTH,
                source_id=self.source_id,
                payload=health_payload
            )

            await bus.publish(event)
            await asyncio.sleep(2)
        