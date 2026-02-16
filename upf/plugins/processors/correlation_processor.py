from upf.core.events import BaseEvent

class CorrelationProcessor:

    @property
    def supported_event_types(self):
        return ["AlertEvent", "SystemHealthEvent"]
    
    def __init__(self):
        self.last_health_status = None

    async def process(self, event, bus):

        #Αν είναι health event, ενημερώνουμε κατάσταση
        if event.event_type == "SystemHealthEvent":
            self.last_health_status = event.payload.get("status")
            return
        
        #Αν είναι alert event
        if event.event_type == "AlertEvent":

            #Φιλτράρουμε μόνο alerts από temporal_aggregator
            if event.source_id != "temporal_aggregator":
                return

            #Ελέγχομυε health condition
            if self.last_health_status == "OK":

                correlated_alert = BaseEvent.create(
                    event_type="CorrelatedAlertEvent",
                    source_id="correlation_processor",
                    payload={
                        "message": "Correlated Alert",
                        "original_alert": event.payload
                    },
                    correlation_id=event.event_id
                )

                await bus.publish(correlated_alert)