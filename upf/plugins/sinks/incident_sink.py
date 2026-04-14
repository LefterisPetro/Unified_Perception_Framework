from upf.core.event_types import EventType
from upf.utilities.serialization import serialize_payload

class IncidentSink:
    @property
    def supported_event_types(self):
        return [EventType.INCIDENT_UPDATE]
    
    async def handle(self, event):
        payload = serialize_payload(event.payload)
        print(f"INCIDENT {payload['status']}: {payload['label']} sensors={payload['sensors']} confidence={payload['confidence']} incident_id={payload['incident_id'][:8]}")