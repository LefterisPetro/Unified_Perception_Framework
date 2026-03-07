from upf.core.events import BaseEvent
from upf.core.event_types import EventType
from upf.core.event_payloads import ScoredAlertPayload

class RuleBasedScoringProcessor:
    @property
    def supported_event_types(self):
        return [EventType.VISION_ALERT]
    
    def __init__(self, rules: dict):
        """
        rules example:
        {
          "fire":  {"base":0.8, "hit_weight":0.05, "severity":"HIGH"},
          "smoke": {"base":0.55, "hit_weight":0.07, "severity":"MEDIUM"},
          "drone": {"base":0.60, "hit_weight":0.06, "severity":"MEDIUM"},
        }
        """
        self.rules = rules

    async def process(self, event, bus):
        payload = event.payload # Assuming payload is a VisionAlertPayload
        label = payload.label # "fire", "smoke", "drone"

        rule = self.rules.get(label)
        if not rule:
            return # No rule for this label, ignore
        
        base = float(rule.get("base", 0.5))
        hit_weight = float(rule.get("hit_weight", 0.05))
        severity = str(rule.get("severity", "LOW"))

        confidence = min(1.0, base + payload.hits * hit_weight)

        scored_payload = ScoredAlertPayload(
            original_alert=payload, # Keep typed evidence of the original alert payload
            confidence=round(confidence, 2),
            severity=severity
        )

        scored_event = BaseEvent.create(
            event_type=EventType.SCORED_ALERT,
            source_id="rule_based_scoring_processor",
            payload=scored_payload,
            correlation_id=event.event_id
        )

        await bus.publish(scored_event)