class ConsoleSink:

    @property
    def supported_event_types(self):
        return[
            "MeasurementEvent",
            "AlertEvent",
            "SystemHealthEvent"
        ]

    async def handle(self, event):
        print(
            f"[{event.event_type}] "
            f"id={event.event_id[:8]} "
            f"corr={event.correlation_id} "
            f"from {event.source_id} "
            f" -> {event.payload}"
            )