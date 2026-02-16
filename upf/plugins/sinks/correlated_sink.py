from upf.core.event_types import EventType

class CorrelatedAlertSink:

    @property
    def supported_event_types(self):
        return[EventType.CORRELATED_ALERT]
    
    async def handle(self, event):
        print("### CORRELATED ALERT:", event.payload)
        