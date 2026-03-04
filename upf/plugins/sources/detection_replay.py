import asyncio
import json
from upf.core.events import BaseEvent
from upf.core.event_types import EventType
from upf.core.event_payloads import DetectionPayload, BBoxPayload

class DetectionReplaySource:
    def __init__(self, file_path, source_id="detection_replay"):
        self.file_path = file_path
        self.source_id = source_id

    async def start(self, bus):
        with open(self.file_path, "r") as f:
            for line in f:
                data = json.loads(line.strip())

                bbox = None
                if "bbox" in data and data["bbox"] is not None:
                    bbox = BBoxPayload(**data["bbox"])

                det_payload = DetectionPayload(
                    label=data["label"],
                    confidence=float(data["confidence"]),
                    bbox=bbox,
                    camera_id=data.get("camera_id")
                )

                event = BaseEvent.create(
                    event_type=EventType.DETECTION,
                    payload=det_payload,        
                    source_id=self.source_id
                )

                await bus.publish(event)
                await asyncio.sleep(0.2)  # Simulate delay between events