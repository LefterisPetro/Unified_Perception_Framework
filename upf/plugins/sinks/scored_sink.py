from upf.core.event_types import EventType

class ScoredAlertSink:

    @property
    def supported_event_types(self):
        return [EventType.SCORED_ALERT]
    
    async def handle(self, event):
        print("### SCORED ALERT:", event.payload)