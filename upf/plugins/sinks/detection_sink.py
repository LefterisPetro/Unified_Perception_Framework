from upf.core.event_types import EventType
from upf.utilities.serialization import serialize_payload

class DetectionSink:
    @property
    def supported_event_types(self):
        return [EventType.DETECTION]
    
    async def handle(self, event):
        print("DETECTION:", serialize_payload(event.payload))