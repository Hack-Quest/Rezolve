"""
sse.py — Server-Sent Events streaming for the 4-agent pipeline.

The CLI `run_pipeline()` runs all four agents and returns only the final
envelope, so it can't drive a per-stage UI. This module re-runs the same
four agent functions but YIELDS an event after each one, so the frontend
can light up Scout -> Investigator -> Impact -> Commander in real time.

The agent functions are synchronous and blocking (httpx.Client + Ollama
timeout). We keep this a SYNC generator on purpose: Starlette's
StreamingResponse iterates sync generators in a threadpool, so the blocking
LLM calls never freeze the event loop.
"""
import json
import time
import logging
from pathlib import Path
from typing import Iterator

from backend.app.agents.scout import scout_alert
from backend.app.agents.investigator import investigate_scout_output
from backend.app.agents.impact import assess_impact
from backend.app.agents.commander import generate_command
from backend.app.models.schemas import PipelineResults

logger = logging.getLogger("decision_platform.sse")

# Same anchoring trick the tools use: resolve relative to THIS file, not CWD,
# so it works no matter where uvicorn is launched from.
# api -> app -> backend -> project root
ALERTS_FILE = Path(__file__).resolve().parents[3] / "shared" / "data" / "sample_alerts.json"


def load_alert_text(alert_id: str) -> str:
    """Look up a sample alert's raw_log by id (e.g. 'alert-001')."""
    with open(ALERTS_FILE) as f:
        alerts = json.load(f)["alerts"]
    for a in alerts:
        if a["id"] == alert_id:
            return a["raw_log"]
    raise KeyError(alert_id)


def _sse(event: str, data: dict) -> str:
    """Format one SSE frame. Named events so the frontend can addEventListener."""
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


def stream_pipeline(raw_alert: str) -> Iterator[str]:
    """
    Run the 4 agents one at a time, emitting an SSE event after each.

    Event sequence:
      pipeline_start          -> the raw alert is in flight
      agent_start  (x4)       -> {agent} is now thinking (drives the spinner)
      agent_complete (x4)     -> {agent, output, elapsed_s} (fills the card)
      pipeline_complete       -> full PipelineResults envelope + total time
      pipeline_error          -> {stage, message} if anything throws
    """
    t0 = time.time()
    yield _sse("pipeline_start", {"raw_alert": raw_alert})

    try:
        # --- Scout -----------------------------------------------------
        yield _sse("agent_start", {"agent": "scout"})
        ts = time.time()
        scout = scout_alert(raw_alert)
        yield _sse("agent_complete", {
            "agent": "scout",
            "elapsed_s": round(time.time() - ts, 1),
            "output": scout.model_dump(),
        })

        # --- Investigator ----------------------------------------------
        yield _sse("agent_start", {"agent": "investigator"})
        ts = time.time()
        investigator = investigate_scout_output(scout)
        yield _sse("agent_complete", {
            "agent": "investigator",
            "elapsed_s": round(time.time() - ts, 1),
            "output": investigator.model_dump(),
        })

        # --- Impact (the wow) ------------------------------------------
        yield _sse("agent_start", {"agent": "impact"})
        ts = time.time()
        impact = assess_impact(scout, investigator, raw_alert)
        yield _sse("agent_complete", {
            "agent": "impact",
            "elapsed_s": round(time.time() - ts, 1),
            "output": impact.model_dump(),
        })

        # --- Commander -------------------------------------------------
        yield _sse("agent_start", {"agent": "commander"})
        ts = time.time()
        commander = generate_command(investigator, impact)
        yield _sse("agent_complete", {
            "agent": "commander",
            "elapsed_s": round(time.time() - ts, 1),
            "output": commander.model_dump(),
        })

        # --- Final envelope --------------------------------------------
        envelope = PipelineResults(
            scout=scout,
            investigator=investigator,
            impact=impact,
            commander=commander,
        )
        yield _sse("pipeline_complete", {
            "total_s": round(time.time() - t0, 1),
            "results": envelope.model_dump(),
        })

    except Exception as e:  # never crash the stream mid-demo
        logger.exception("pipeline failed")
        yield _sse("pipeline_error", {"message": f"{type(e).__name__}: {e}"})