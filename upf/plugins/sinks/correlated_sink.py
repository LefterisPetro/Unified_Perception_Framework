from upf.core.event_types import EventType
from upf.utilities.serialization import serialize_payload

class CorrelatedAlertSink:

    @property
    def supported_event_types(self):
        return[EventType.CORRELATED_ALERT]
    
    async def handle(self, event):
        print("### CORRELATED ALERT:", serialize_payload(event.payload))
        