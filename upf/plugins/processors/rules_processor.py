from upf.core.events import BaseEvent

class RulesProcessor:

    @property
    def supported_event_types(self):
        return["MeasurementEvent"]

    def __init__(self, threshold):
        self.threshold = threshold
        self.active = False

    async def process(self, event, bus):
        value = event.payload.get("value")
        if value is None:
            return
        
        if value > self.threshold and not self.active:
            self.active = True

            alert = BaseEvent.create(
                event_type="AlertEvent",
                source_id="rules_processor",
                payload={
                    "message": "Threshold exceeded",
                    "value": value
                },
                correlation_id=event.event_id
            )
            
            event.processing_history.append("RulesProcessor")
            await bus.publish(alert)
        
        elif value <= self.threshold:
            self.active = False