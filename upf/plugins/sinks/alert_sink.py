from upf.core.event_types import EventType

class AlertOnlySink:

    @property
    def supported_event_types(self):
        return[EventType.ALERT]
    
    async def handle(self, event):
        print(">>> ALERT RECEIVED:", event.payload)