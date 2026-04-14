import asyncio
import json

from upf.core.events import BaseEvent
from upf.core.event_types import EventType
from upf.core.event_payloads import ThermalCuePayload

class ThermalCueReplaySource:
    def __init__(self, file_path, source_id="thermal_cue_replay"):
        self.file_path = file_path
        self.source_id = source_id

    async def start(self, bus):
        with open(self.file_path, "r") as f:
            for line in f:
                data = json.loads(line.strip())

                payload = ThermalCuePayload(
                    confidence=float(data["confidence"]),
                    camera_id=data.get("camera_id"),
                    note=data.get("note"),
                )

                event = BaseEvent.create(
                    event_type=EventType.THERMAL_CUE,
                    source_id=self.source_id,
                    payload=payload
                )

                await bus.publish(event)
                await asyncio.sleep(0.2) # small delay to simulate real-time streaming
                