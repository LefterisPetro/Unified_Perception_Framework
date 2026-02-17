from upf.core.event_types import EventType
from upf.core.events import BaseEvent

class ScoringProcessor:

    @property
    def supported_event_types(self):
        return [EventType.ALERT]
    
    def __init__(self, base_confidence: float = 0.5):
        self.base_confidence = base_confidence

    async def process(self, event, bus):

        #Simple scoring based on count evidence
        count = event.payload.get("count", 1)

        confidence = min(1.0, self.base_confidence + (count * 0.1))

        if confidence >= 0.8:
            severity = "HIGH"
        elif confidence >= 0.6:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        scored_event = BaseEvent.create(
            event_type=EventType.SCORED_ALERT,
            source_id="scoring_processor",
            payload={
                "original_alert": event.payload,
                "confidence": round(confidence, 2),
                "severity": severity
            },
            correlation_id=event.event_id
        )

        await bus.publish(scored_event)