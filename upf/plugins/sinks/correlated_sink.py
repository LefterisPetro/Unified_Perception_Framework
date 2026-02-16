class CorrelatedAlertSink:

    @property
    def supported_event_types(self):
        return["CorrelatedAlertEvent"]
    
    async def handle(self, event):
        print("### CORRELATED ALERT:", event.payload)
        