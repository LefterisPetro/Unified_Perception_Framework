import json
import sqlite3
import time
from typing import List, Dict, Any
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

DB_PATH = "data/upf_incidents.db"

app = FastAPI()

def db_connect():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def get_latest_incidents(limit: int = 50) -> List[Dict[str, Any]]:
    """
    Returns latest state per incident_id based on the newest row for each incident_id.
    """
    conn = db_connect()
    rows = conn.execute(
        """
        SELECT t.*
        FROM incident_updates t
        JOIN (
          SELECT incident_id, MAX(id) AS max_id
          FROM incident_updates
          GROUP BY incident_id
        ) latest
        ON t.incident_id = latest.incident_id AND t.id = latest.max_id
        ORDER BY t.id DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    conn.close()

    out = []
    for r in rows:
        out.append(
            {
                "id": r["id"],
                "incident_id": r["incident_id"],
                "label": r["label"],
                "status": r["status"],
                "confidence": r["confidence"],
                "created_at": r["created_at"],
                "sensors": json.loads(r["sensors_json"]) if r["sensors_json"] else [],
            }
        )
    return out


def get_recent_updates(limit: int = 100) -> List[Dict[str, Any]]:
    conn = db_connect()
    rows = conn.execute(
        """
        SELECT id, incident_id, label, status, confidence, created_at, sensors_json
        FROM incident_updates
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    conn.close()

    out = []
    for r in rows:
        out.append(
            {
                "id": r["id"],
                "incident_id": r["incident_id"],
                "label": r["label"],
                "status": r["status"],
                "confidence": r["confidence"],
                "created_at": r["created_at"],
                "sensors": json.loads(r["sensors_json"]) if r["sensors_json"] else [],
            }
        )
    return out


@app.get("/api/incidents")
def api_incidents(limit: int = 50):
    return {"incidents": get_latest_incidents(limit)}


@app.get("/api/history")
def api_history(limit: int = 100):
    return {"updates": get_recent_updates(limit)}


@app.websocket("/ws")
async def ws_incidents(ws: WebSocket):
    await ws.accept()

    last_id = 0
    try:
        while True:
            # poll DB for new rows (simple MVP)
            conn = db_connect()
            rows = conn.execute(
                """
                SELECT id, incident_id, label, status, confidence, created_at, sensors_json
                FROM incident_updates
                WHERE id > ?
                ORDER BY id ASC
                """,
                (last_id,),
            ).fetchall()
            conn.close()

            for r in rows:
                last_id = max(last_id, r["id"])
                msg = {
                    "type": "update",
                    "row": {
                        "id": r["id"],
                        "incident_id": r["incident_id"],
                        "label": r["label"],
                        "status": r["status"],
                        "confidence": r["confidence"],
                        "created_at": r["created_at"],
                        "sensors": json.loads(r["sensors_json"]) if r["sensors_json"] else [],
                    },
                }
                await ws.send_text(json.dumps(msg))

            await ws.send_text(json.dumps({"type": "heartbeat", "ts": time.time()}))
            await asyncio_sleep(0.5)
    except Exception:
        # client disconnected or server stopped
        return


async def asyncio_sleep(sec: float):
    import asyncio
    await asyncio.sleep(sec)


@app.get("/")
def index():
    # Minimal single-page UI (no external libs)
    html = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>UPF Dashboard (MVP)</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 18px; }
    .row { display: flex; gap: 16px; }
    .card { border: 1px solid #ddd; border-radius: 10px; padding: 12px; width: 48%; }
    table { width: 100%; border-collapse: collapse; font-size: 14px; }
    th, td { border-bottom: 1px solid #eee; padding: 8px; text-align: left; }
    th { background: #fafafa; position: sticky; top: 0; }
    .badge { padding: 2px 8px; border-radius: 10px; font-size: 12px; display: inline-block; }
    .POSSIBLE { background: #fff2cc; }
    .CONFIRMED { background: #d9ead3; }
    .LOST { background: #f4cccc; }
    .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 12px; }
  </style>
</head>
<body>
  <h2>UPF Dashboard (MVP)</h2>
  <div class="row">
    <div class="card">
      <h3>Live Incidents</h3>
      <table id="live">
        <thead>
          <tr><th>Status</th><th>Label</th><th>Confidence</th><th>Sensors</th><th>Incident</th></tr>
        </thead>
        <tbody></tbody>
      </table>
    </div>
    <div class="card">
      <h3>Recent Updates</h3>
      <table id="hist">
        <thead>
          <tr><th>ID</th><th>Status</th><th>Label</th><th>Confidence</th><th>Sensors</th><th>Incident</th></tr>
        </thead>
        <tbody></tbody>
      </table>
    </div>
  </div>

<script>
const liveBody = document.querySelector("#live tbody");
const histBody = document.querySelector("#hist tbody");
const liveMap = new Map(); // incident_id -> row data

function shortId(x) { return (x || "").slice(0, 8); }

function renderLive() {
  liveBody.innerHTML = "";
  const items = Array.from(liveMap.values()).sort((a,b)=> b.id - a.id);
  for (const r of items) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><span class="badge ${r.status}">${r.status}</span></td>
      <td>${r.label}</td>
      <td>${r.confidence.toFixed(2)}</td>
      <td>${(r.sensors||[]).join(", ")}</td>
      <td class="mono" title="${r.incident_id}">${shortId(r.incident_id)}</td>
    `;
    liveBody.appendChild(tr);
  }
}

function addHistoryRow(r) {
  const tr = document.createElement("tr");
  tr.innerHTML = `
    <td class="mono">${r.id}</td>
    <td><span class="badge ${r.status}">${r.status}</span></td>
    <td>${r.label}</td>
    <td>${r.confidence.toFixed(2)}</td>
    <td>${(r.sensors||[]).join(", ")}</td>
    <td class="mono" title="${r.incident_id}">${shortId(r.incident_id)}</td>
  `;
  histBody.prepend(tr);
  // limit rows
  while (histBody.children.length > 50) histBody.removeChild(histBody.lastChild);
}

async function bootstrap() {
  const inc = await fetch("/api/incidents").then(r=>r.json());
  for (const r of inc.incidents) liveMap.set(r.incident_id, r);
  renderLive();

  const hist = await fetch("/api/history").then(r=>r.json());
  for (const r of hist.updates.reverse()) addHistoryRow(r);

  const ws = new WebSocket(`ws://${location.host}/ws`);
  ws.onmessage = (ev) => {
    const msg = JSON.parse(ev.data);
    if (msg.type === "update") {
      const r = msg.row;
      liveMap.set(r.incident_id, r);
      renderLive();
      addHistoryRow(r);
    }
  };
}

bootstrap();
</script>
</body>
</html>
"""
    return HTMLResponse(html)