from upf.core.event_types import EventType
from upf.utilities.serialization import serialize_payload

class ConsoleSink:

    @property
    def supported_event_types(self):
        return[EventType.MEASUREMENT,
               EventType.ALERT,
               EventType.SYSTEM_HEALTH,
               EventType.CORRELATED_ALERT,
               EventType.FUSION_READY_ALERT,
               EventType.METRICS_SNAPSHOT,
               EventType.DETECTION,
               EventType.RF_CUE
               ]

    async def handle(self, event):

        payload_out = serialize_payload(event.payload)

        print(
            f"[{event.event_type.value}] "
            f"id={event.event_id[:8]} "
            f"corr={event.correlation_id} "
            f"from {event.source_id} "
            f" -> {payload_out}"
            )