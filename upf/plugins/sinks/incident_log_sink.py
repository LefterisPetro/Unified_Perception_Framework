import json
import sqlite3
import time
from pathlib import Path

from upf.core.event_types import EventType
from upf.utilities.serialization import serialize_payload

class IncidentLogSink:
    """
    A sink that logs incidents (IncidentUpdateEvents) to a SQLite local database.
    This sink is designed to store incident data in a structured format, allowing for easy querying and analysis.
    """

    @property
    def supported_event_types(self):
        return [EventType.INCIDENT_UPDATE]
    
    def __init__(self, db_path: str = "incident_log.db"):
        self.db_path = str(db_path)
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True) if Path(self.db_path).parent.as_posix() not in (".", "") else None

        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.execute("PRAGMA journal_mode=WAL;")  # Enable Write-Ahead Logging for better concurrency
        self.conn.execute("PRAGMA synchronous=NORMAL;")  # Set synchronous mode to NORMAL for better performance
        self._ensure_schema()

    def _ensure_schema(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS incident_updates (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               created_at REAL NOT NULL,
               incident_id REAL NOT NULL,
               label TEXT NOT NULL,
               status TEXT NOT NULL,
               confidence REAL NOT NULL,
               sensors_json TEXT NOT NULL,
               first_seen REAL,
               last_seen REAL,
               evidence_count INTEGER,
               payload_json TEXT NOT NULL
            );
            """
        )
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_incident_id ON incident_updates(incident_id);")
        self.conn.execute("CREATE INDEX IF NOT EXISTS idx_created_at ON incident_updates(created_at);")
        self.conn.commit()

    async def handle(self, event):
        payload = serialize_payload(event.payload)
        created_at = time.time()
        sensors_json = json.dumps(payload.get("sensors", []), ensure_ascii=False)
        payload_json = json.dumps(payload, ensure_ascii=False)

        self.conn.execute(
            """
            INSERT INTO incident_updates
            (created_at, incident_id, label, status, confidence, sensors_json, first_seen, last_seen, evidence_count, payload_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """,
            (
                created_at,
                payload.get("incident_id"),
                payload.get("label"),
                payload.get("status"),
                float(payload.get("confidence", 0.0)),
                sensors_json,
                float(payload.get("first_seen", 0.0)) if payload.get("first_seen") is not None else None,
                float(payload.get("last_seen", 0.0)) if payload.get("last_seen") is not None else None,
                int(payload.get("evidence_count", 0)) if payload.get("evidence_count") is not None else None,
                payload_json
                ),
        )
        self.conn.commit()