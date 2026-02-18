from upf.core.events import BaseEvent
from upf.core.event_types import EventType
from upf.core.event_payloads import CorrelatedAlertPayload

class CorrelationProcessor:

    @property
    def supported_event_types(self):
        return [EventType.FUSION_READY_ALERT, EventType.SYSTEM_HEALTH]
    
    def __init__(self):
        self.last_health_status = None

    async def process(self, event, bus):

        #Αν είναι health event, ενημερώνουμε κατάσταση
        if event.event_type == EventType.SYSTEM_HEALTH:
            self.last_health_status = event.payload.status
            return
        
        #Αν είναι alert event
        if event.event_type == EventType.FUSION_READY_ALERT:

            #Φιλτράρουμε μόνο alerts από temporal_aggregator
            if event.source_id != "fusion_gate_processor":
                return


            #Ελέγχομυε health condition
            if self.last_health_status == "OK":

                correlated_payload = CorrelatedAlertPayload(
                    message="Correlated Alert",
                    original_alert=event.payload
                )

                correlated_alert = BaseEvent.create(
                    event_type=EventType.CORRELATED_ALERT,
                    source_id="correlation_processor",
                    payload=correlated_payload,
                    correlation_id=event.event_id
                )

                await bus.publish(correlated_alert)