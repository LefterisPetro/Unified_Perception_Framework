import asyncio
import json

from upf.core.events import BaseEvent
from upf.core.event_types import EventType
from upf.core.event_payloads import RFCuePayload

class RFCueReplaySource:
    def __init__(self, file_path, source_id="rf_cue_replay"):
        self.file_path = file_path
        self.source_id = source_id

    async def start(self, bus):
        with open(self.file_path, "r") as f:
            for line in f:
                data = json.loads(line.strip())

                rf_payload = RFCuePayload( 
                    band_hz=float(data["band_hz"]),
                    center_freq_hz=float(data["center_freq_hz"]),
                    bandwidth_hz=float(data["bandwidth_hz"]),
                    snr_db=float(data["snr_db"]),
                    confidence=float(data["confidence"]),
                    sensor_id=data.get("sensor_id", "hackrf"),
                    note=data.get("note")
                )

                event = BaseEvent.create(
                    event_type=EventType.RF_CUE,
                    source_id=self.source_id,
                    payload=rf_payload
                )

                await bus.publish(event)
                await asyncio.sleep(0.2) # small delay to simulate real-time streaming