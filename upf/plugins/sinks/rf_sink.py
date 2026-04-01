from upf.core.event_types import EventType
from upf.utilities.serialization import serialize_payload

class RFCueSink:

    @property
    def supported_event_types(self):
        return[EventType.RF_CUE]

    async def handle(self, event):
        print("RF Cue:", serialize_payload(event.payload))
