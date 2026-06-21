"""
main.py — FastAPI entrypoint.

Run from the PROJECT ROOT (so `backend` imports as a package, same as the CLI):

    uvicorn backend.app.main:app --reload --port 8000

Endpoints:
    GET /api/health                      -> {"ok": true}
    GET /api/stream?alert_id=alert-001   -> SSE stream (replay a sample alert)
    GET /api/stream?raw_alert=...        -> SSE stream (free-text alert)
"""
import logging

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from backend.app.api.sse import stream_pipeline, load_alert_text

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Decision Intelligence Platform")

# Next.js dev server runs on a different origin; EventSource needs CORS.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # tighten/loosen as needed
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"ok": True}


@app.get("/api/stream")
def stream(
    alert_id: str | None = Query(default=None, description="e.g. alert-001"),
    raw_alert: str | None = Query(default=None, description="free-text alert"),
):
    """
    Native browser EventSource is GET-only and can't send a body, so the alert
    arrives as a query param. For the demo you replay canned alerts by id; the
    server looks up the raw_log. Free-text is supported too.
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
        stream_pipeline(text),
        media_type="text/event-stream",
        headers=headers,
    )