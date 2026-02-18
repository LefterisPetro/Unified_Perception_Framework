from upf.core.event_types import EventType
from upf.utilities.serialization import serialize_payload

class AlertOnlySink:

    @property
    def supported_event_types(self):
        return[EventType.ALERT]
    
    async def handle(self, event):
        print(">>> ALERT RECEIVED:", serialize_payload(event.payload))