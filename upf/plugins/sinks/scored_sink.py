from upf.core.event_types import EventType
from upf.utilities.serialization import serialize_payload

class ScoredAlertSink:

    @property
    def supported_event_types(self):
        return [EventType.SCORED_ALERT]
    
    async def handle(self, event):
        print("### SCORED ALERT:", serialize_payload(event.payload))