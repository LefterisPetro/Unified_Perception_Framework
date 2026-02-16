class AlertOnlySink:

    @property
    def supported_event_types(self):
        return["AlertEvent"]
    
    async def handle(self, event):
        print(">>> ALERT RECEIVED:", event.payload)