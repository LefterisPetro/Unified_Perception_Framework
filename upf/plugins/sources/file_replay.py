import asyncio
import json
from upf.core.events import BaseEvent
from upf.core.event_types import EventType
from upf.core.event_payloads import MeasurementPayload

class FileReplaySource:
    def __init__(self, file_path, source_id="file_replay"):
        self.file_path = file_path
        self.source_id = source_id

    async def start(self, bus):
        with open(self.file_path, "r") as f:
            for line in f:
                data = json.loads(line.strip())

                measurement_payload = MeasurementPayload(value=data["value"])

                event = BaseEvent.create(
                    event_type=EventType.MEASUREMENT,
                    source_id=self.source_id,
                    payload=measurement_payload
                )

                await bus.publish(event)
                await asyncio.sleep(0.5)
                