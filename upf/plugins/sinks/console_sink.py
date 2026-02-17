from upf.core.event_types import EventType

class ConsoleSink:

    @property
    def supported_event_types(self):
        return[EventType.MEASUREMENT,
               EventType.ALERT,
               EventType.SYSTEM_HEALTH,
               EventType.CORRELATED_ALERT,
               EventType.FUSION_READY_ALERT
               ]

    async def handle(self, event):
        print(
            f"[{event.event_type.value}] "
            f"id={event.event_id[:8]} "
            f"corr={event.correlation_id} "
            f"from {event.source_id} "
            f" -> {event.payload}"
            )