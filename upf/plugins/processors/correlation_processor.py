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
 
            if event.source_id not in ("fusion_gate_processor", "rf_fusion_processor"):
                return # Αν το alert δεν προέρχεται από τους επιτρεπόμενους επεξεργαστές, αγνοούμε το event


            if self.last_health_status == "OK": # Αν η τελευταία κατάσταση υγείας είναι OK, προχωράμε με τη συσχέτιση

                correlated_payload = CorrelatedAlertPayload( # Δημιουργία payload για το συσχετισμένο alert
                    message="Correlated Alert", 
                    original_alert=event.payload 
                )

                correlated_alert = BaseEvent.create( # Δημιουργία του συσχετισμένου alert event
                    event_type=EventType.CORRELATED_ALERT, # Ορίζουμε τον τύπο του event ως CORRELATED_ALERT
                    source_id="correlation_processor", # Ορίζουμε το source_id ως correlation_processor για να γνωρίζουμε την προέλευση του event
                    payload=correlated_payload, # Το payload περιέχει το συσχετισμένο alert
                    correlation_id=event.event_id # Χρησιμοποιούμε το event_id του αρχικού alert ως correlation_id για να διατηρήσουμε τη συσχέτιση μεταξύ των events
                )

                await bus.publish(correlated_alert)