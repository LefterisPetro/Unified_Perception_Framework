from upf.core.event_types import EventType
from upf.core.events import BaseEvent

class FusionGateProcessor:

    @property
    def supported_event_types(self):
        return [EventType.SCORED_ALERT]
    
    def __init__(self, min_confidence: float = 0.6):
        self.min_confidence = min_confidence
    
    async def process(self, event, bus):

        confidence = float(event.payload.get("confidence", 0))

        if confidence < self.min_confidence:
            return #Drop low confidence alerts
        
        fusion_event = BaseEvent.create(
            event_type=EventType.FUSION_READY_ALERT,
            source_id="fusion_gate_processor",
            payload=event.payload,
            correlation_id=event.event_id
        )

        await bus.publish(fusion_event)