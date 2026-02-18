from upf.core.event_types import EventType
from upf.core.events import BaseEvent
from upf.core.event_payloads import FusionReadyPayload

class FusionGateProcessor:

    @property
    def supported_event_types(self):
        return [EventType.SCORED_ALERT]
    
    def __init__(self, min_confidence: float = 0.6):
        self.min_confidence = min_confidence
    
    async def process(self, event, bus):

        confidence = event.payload.confidence

        if confidence < self.min_confidence:
            return #Drop low confidence alerts
        
        fusion_payload = FusionReadyPayload(
            original_alert=event.payload,
            confidence=confidence,
            severity=event.payload.severity
        )

        fusion_event = BaseEvent.create(
            event_type=EventType.FUSION_READY_ALERT,
            source_id="fusion_gate_processor",
            payload=fusion_payload,
            correlation_id=event.event_id
        )

        await bus.publish(fusion_event)