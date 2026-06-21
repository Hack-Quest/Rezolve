"""
main.py — FastAPI entrypoint.

Run from the PROJECT ROOT (so `backend` imports as a package, same as the CLI):

    uvicorn backend.app.main:app --reload --port 8000

Endpoints:
    GET /api/health                      -> {"ok": true}
    GET /api/alerts                      -> list of all alerts in the store
    GET /api/alerts/{alert_id}           -> single alert, with pipeline_results if processed
    GET /api/stream?alert_id=alert-001   -> SSE stream (replay a sample alert)
    GET /api/stream?raw_alert=...        -> SSE stream (free-text alert)
"""
import logging
from contextlib import asynccontextmanager
import anyio

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from backend.app.api.sse import stream_pipeline, load_alert_text
from backend.app.agents.warmup import warm_at_startup
from backend.app.models.store import store, StoredAlert

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pre-load the big model (llama3:8b) the moment the server boots, so the
    # FIRST alert run during the live demo doesn't eat a cold-load penalty.
    # Blocks synchronously in a worker thread before the app is ready to accept requests.
    await anyio.to_thread.run_sync(warm_at_startup)
    yield


app = FastAPI(title="Decision Intelligence Platform", lifespan=lifespan)

# Next.js dev server runs on a different origin; EventSource needs CORS.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Next.js / Vite dev
    allow_methods=["GET"],
    allow_headers=["*"],
)


# Pre-seed the in-memory alert store on startup.
# Done at import time (not in a lifespan handler) for simplicity — the store
# is in-memory only, so there's no async I/O to wait for.
store.seed_from_sample_file()


@app.get("/api/health")
def health():
    return {"ok": True}


@app.get("/api/alerts", response_model=list[StoredAlert])
def list_alerts():
    """
    Return every alert in the store, ordered by id.
    Includes processed_at and pipeline_results if the alert has been run
    through the pipeline; otherwise those fields are null.
    """
    return store.list_alerts()


@app.get("/api/alerts/{alert_id}", response_model=StoredAlert)
def get_alert(alert_id: str):
    """Return one alert by id. 404 if not in the store."""
    alert = store.get_alert(alert_id)
    if alert is None:
        raise HTTPException(404, f"alert '{alert_id}' not found")
    return alert


@app.get("/api/stream")
def stream(
    alert_id: str | None = Query(default=None, description="e.g. alert-001"),
    raw_alert: str | None = Query(default=None, description="free-text alert"),
):
    """
    Native browser EventSource is GET-only and can't send a body, so the alert
    arrives as a query param. For the demo you replay canned alerts by id; the
    server looks up the raw_log. Free-text is supported too.

    When alert_id is provided, the pipeline's final results are also persisted
    to the in-memory store (so /api/alerts/{id} returns them after the stream
    completes).
    """
    if alert_id:
        try:
            text = load_alert_text(alert_id)
        except KeyError:
            raise HTTPException(404, f"alert '{alert_id}' not found")
    elif raw_alert:
        text = raw_alert
    else:
        raise HTTPException(400, "pass either alert_id or raw_alert")

    headers = {
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "X-Accel-Buffering": "no",  # stop nginx/proxies from buffering the stream
    }
    return StreamingResponse(
        stream_pipeline(text, alert_id=alert_id),
        media_type="text/event-stream",
        headers=headers,
    )