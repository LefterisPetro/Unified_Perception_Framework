import time
import uuid
from typing import Any, Dict, List

from upf.core.events import BaseEvent
from upf.core.event_types import EventType
from upf.core.event_payloads import SensorCuePayload, IncidentUpdatePayload

class IncidentManagerProcessor:
    @property
    def supported_event_types(self): 
        return [EventType.SENSOR_CUE, EventType.TICK] # This processor will handle incoming sensor cues and periodic tick events to manage the lifecycle of incidents
    
    def __init__( 
            self,
            match_window_seconds: float = 3.0, # Time window to consider sensor cues as part of the same incident
            lifetime_seconds: float = 10.0, # Lifetime for an incident before it is considered resolved
            confirm_min_sensors_by_label: dict | None = None, # Minimum number of unique sensors required to confirm an incident for each label (e.g., {"drone": 2} means at least 2 unique sensors must report a "drone" cue to confirm an incident
    ):
        self.match_window_seconds = float(match_window_seconds)
        self.lifetime_seconds = float(lifetime_seconds)
        self.confirm_min_sensors_by_label = confirm_min_sensors_by_label or {"drone": 2}

        self.incidents: Dict[str, Dict[str, Any]] = {} # Active incidents being tracked

    def _min_sensors(self, label: str) -> int: # Helper method to get the minimum number of unique sensors required to confirm an incident for a given label
        return int(self.confirm_min_sensors_by_label.get(label, 2)) # Default to 2 if not specified
    
    def _cleanup(self): # Internal method to clean up expired incidents based on lifetime
        now = time.time() 
        to_expire = [] # List of incident IDs that should be marked as "LOST" due to exceeding lifetime
        for incident_id, incident in self.incidents.items(): # Iterate through active incidents to check if any have exceeded their lifetime
            if now - incident["last_seen"] > self.lifetime_seconds and incident["status"] != "LOST": # If the current time minus the last seen time of the incident exceeds the lifetime threshold and the incident is not already marked as "LOST"
                to_expire.append(incident_id) # Add the incident ID to the list of incidents to expire

        for incident_id in to_expire: # Iterate through the list of incident IDs that should be expired
            incident = self.incidents[incident_id] # Retrieve the incident data for the incident ID
            incident["status"] = "LOST" # Mark the incident as "LOST" to indicate it is no longer active
                
    def _find_match(self, cue: SensorCuePayload) -> str | None: # Internal method to find a matching incident for a given sensor cue
        now = time.time() 
        candidates = [] # List of matching incidents
        for incident_id, incident in self.incidents.items(): # Iterate through active incidents to find a match for the incoming sensor cue
            if incident["status"] == "LOST": # Skip incidents that are already marked as "LOST"
                continue
            if incident["label"] != cue.label: # Skip incidents that do not match the label of the sensor cue
                continue
            if now - incident["last_seen"] > self.match_window_seconds: # Skip incidents that have not been updated within the match window
                continue
            if cue.camera_id is not None and incident.get("camera_id") is not None: # If both the cue and the incident have a camera_id, check if they match
                if cue.camera_id != incident["camera_id"]: # If the camera IDs do not match, skip this incident
                    continue 
            candidates.append((incident["last_seen"], incident_id)) # If the incident matches the criteria, add it to the list of candidates with its last seen time and ID

        if not candidates: # If no matching incidents were found, return None
            return None
        candidates.sort(reverse=True) # Sort the candidates by last seen time in descending order to prioritize the most recently updated incident
        return candidates[0][1] # Return the ID of the most recently updated matching incident
    
    async def _expire_and_emit_lost(self, bus): # Internal method to check for incidents that have exceeded their lifetime and emit updates marking them as "LOST"
        now = time.time()
        for incident_id, incident in self.incidents.items(): # Iterate through active incidents to check if any have exceeded their lifetime and should be marked as "LOST"
            if incident["status"] == "LOST": # Skip incidents that are already marked as "LOST"
                continue
            if now - incident["last_seen"] <= self.lifetime_seconds: # If the current time minus the last seen time of the incident does not exceed the lifetime threshold, skip this incident as it is still active
                continue

            incident["status"] = "LOST" # Mark the incident as "LOST" to indicate it is no longer active
            payload = IncidentUpdatePayload( 
                incident_id=incident_id,
                label=incident["label"],
                status="LOST",
                sensors=sorted(list(incident["sensors"])),
                confidence=round(float(incident.get("confidence", 0.0)), 2),
                first_seen=incident["first_seen"],
                last_seen=incident["last_seen"],
                evidence_count=incident["evidence_count"],
                last_cue=incident.get("last_cue")
            )

            update_event = BaseEvent.create(
                event_type=EventType.INCIDENT_UPDATE,
                source_id="incident_manager",
                payload=payload,
            )
            await bus.publish(update_event)

    async def process(self, event, bus): # Main method to process incoming events, which can be either sensor cues or tick events
        if event.event_type == EventType.TICK: # If the incoming event is a tick event, we want to check for any incidents that have exceeded their lifetime and should be marked as "LOST"
            await self._expire_and_emit_lost(bus) # On each tick event, check for and emit updates for any incidents that have exceeded their lifetime and should be marked as "LOST"
            return

        self._cleanup() # Clean up expired incidents before processing the new event

        cue: SensorCuePayload = event.payload # Extract the sensor cue payload from the incoming event
        now = time.time()
        incident_id = self._find_match(cue) # Attempt to find a matching incident for the incoming sensor cue

        created = False
        if incident_id is None: # If no matching incident was found, create a new incident
            incident_id = str(uuid.uuid4()) # Generate a unique ID for the new incident
            created = True
            self.incidents[incident_id] = { # Initialize the new incident with relevant information from the sensor cue
                "incident_id": incident_id, # Unique identifier for the incident
                "label": cue.label, # Label of the incident, derived from the sensor cue
                "status": "POSSIBLE", # Initial status of the incident is set to "POSSIBLE" until it can be confirmed based on the number of unique sensors reporting the same label
                "sensors": set(), # Set of unique sensor IDs that have reported cues matching this incident
                "first_seen": now, # Timestamp of when the incident was first created
                "last_seen": now, # Timestamp of the most recent sensor cue that matched this incident
                "evidence_count": 0, # Counter for the total number of sensor cues that have matched this incident, used to track the amount of evidence supporting the incident
                "camera_id": cue.camera_id, # Optional camera ID associated with the incident, derived from the sensor cue if available
                }
        incident = self.incidents[incident_id] # Retrieve the incident data for the matched or newly created incident
        incident["last_seen"] = now # Update the last seen timestamp of the incident to the current time
        incident["last_cue"] = cue # Store the most recent sensor cue that matched this incident for reference in the incident update payload

        if cue.camera_id and not incident.get("camera_id"): # If the incoming sensor cue has a camera_id and the incident does not already have a camera_id, associate the camera_id from the cue with the incident
            incident["camera_id"] = cue.camera_id
        
        incident["sensors"].add(cue.sensor_type) # Add the sensor type from the incoming cue to the set of unique sensors that have reported cues matching this incident
        incident["evidence_count"] += 1 # Increment the evidence count for the incident to reflect the new sensor cue that has been associated with it

        incident_confidence = max(float(incident.get("confidence", 0.0)), float(cue.confidence)) # Update the confidence level of the incident to be the maximum of the existing confidence and the confidence from the incoming sensor cue, ensuring that the incident's confidence reflects the strongest evidence supporting it
        incident["confidence"] = incident_confidence # Store the updated confidence level in the incident data

        if incident["status"] != "CONFIRMED": # If the incident is not already confirmed, check if it can be confirmed based on the number of unique sensors reporting cues that match this incident
            if len(incident["sensors"]) >= self._min_sensors(incident["label"]): # If the number of unique sensors that have reported cues matching this incident meets or exceeds the minimum required for confirmation based on the incident's label, update the status of the incident to "CONFIRMED"
                incident["status"] = "CONFIRMED"

        payload = IncidentUpdatePayload( # Create a payload for the incident update event, containing relevant information about the incident
            incident_id=incident_id, # Unique identifier for the incident
            label=incident["label"], # Label of the incident
            status=incident["status"], # Current status of the incident (e.g., "POSSIBLE", "CONFIRMED", "LOST")
            sensors=sorted(list(incident["sensors"])), # Sorted list of unique sensors that have reported cues matching this incident, included in the payload for informational purposes
            confidence=round(incident["confidence"], 2), # Confidence level of the incident, rounded to 2 decimal places for readability
            first_seen=incident["first_seen"], # Timestamp of when the incident was first created, included in the payload for informational purposes
            last_seen=incident["last_seen"], # Timestamp of the most recent sensor cue that matched this incident, included in the payload for informational purposes
            evidence_count=incident["evidence_count"], # Total number of sensor cues that have matched this incident, included in the payload to provide insight into the amount of evidence supporting the incident
            last_cue=cue # Include the most recent sensor cue in the payload to provide context about the latest evidence associated with the incident
        )

        update_event = BaseEvent.create( # Create a new event to represent the update to the incident, which can be published to the event bus for other components to consume
            event_type=EventType.INCIDENT_UPDATE, # The type of the event is set to "INCIDENT_UPDATE" to indicate that this event represents an update to an incident's information
            source_id="incident_manager", # The source ID of the event is set to "incident_manager" to indicate that this event was generated by the IncidentManagerProcessor
            payload=payload, # The payload of the event contains the IncidentUpdatePayload with all relevant information about the incident update
            correlation_id=event.event_id # The correlation ID of the update event is set to the ID of the incoming event that triggered this processing, allowing for traceability and correlation between the original sensor cue event and the resulting incident update event
        )

        await bus.publish(update_event) # Publish the incident update event to the event bus, allowing other components in the system to react to the updated incident information