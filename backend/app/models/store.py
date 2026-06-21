"""
store.py — In-memory alert store.

Holds the 7 pre-seeded sample alerts AND any alerts that have been processed
through the pipeline. Persists for the lifetime of the uvicorn process — no
database, no disk. Restart = fresh state. That's intentional per the
hackathon scope rules ("no persistent user databases").

WHY THIS FILE EXISTS (read before moving it):
The original instinct was to keep `_processed_alerts: dict` in main.py.
That causes a circular import: sse.py needs to write to the store, so it
imports from main.py, but main.py imports sse.py for `stream_pipeline`.
Putting the store in a third module (this one) breaks the cycle. Both
main.py and sse.py import from here — neither imports from the other for
state.

See handover.md Gotcha #4.
"""
from __future__ import annotations

import json
import logging
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from backend.app.models.schemas import PipelineResults

logger = logging.getLogger("decision_platform.store")

# Resolve shared/data/sample_alerts.json relative to THIS file, not CWD.
# Path: store.py -> models -> app -> backend -> project root
_PROJECT_ROOT = Path(__file__).resolve().parents[3]
ALERTS_FILE = _PROJECT_ROOT / "shared" / "data" / "sample_alerts.json"

# How many alerts to pre-seed on startup. The handover says 7.
# If the sample file has fewer, we seed all of them.
SEED_COUNT = 7


class StoredAlert(BaseModel):
    """
    One alert row in the store. Includes both raw input AND (if the pipeline
    has been run on it) the resulting Decision Brief.
    """
    id: str
    title: str
    severity: str
    raw_log: str
    processed_at: Optional[str] = None                # ISO timestamp, None until pipeline runs
    pipeline_results: Optional[PipelineResults] = None


class AlertStore:
    """
    Thread-safe in-memory store.

    uvicorn runs sync StreamingResponse handlers in a threadpool, so multiple
    SSE streams can be running at the same time. We need a lock around
    mutations to avoid dict-corruption races.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._alerts: dict[str, StoredAlert] = {}

    def seed_from_sample_file(self, count: int = SEED_COUNT) -> None:
        """Load the first N sample alerts into the store. Call once on startup."""
        with open(ALERTS_FILE) as f:
            samples = json.load(f)["alerts"]
        seeded = 0
        for sample in samples[:count]:
            alert = StoredAlert(
                id=sample["id"],
                title=sample.get("title", ""),
                severity=sample.get("severity", "UNKNOWN"),
                raw_log=sample["raw_log"],
            )
            self._alerts[alert.id] = alert
            seeded += 1
        logger.info(
            f"AlertStore: seeded {seeded} sample alerts from {ALERTS_FILE.name}"
        )

    def list_alerts(self) -> list[StoredAlert]:
        """Return all alerts, ordered by id (alert-001, alert-002, ...)."""
        with self._lock:
            return sorted(self._alerts.values(), key=lambda a: a.id)

    def get_alert(self, alert_id: str) -> Optional[StoredAlert]:
        """Return one alert by id, or None if not in the store."""
        with self._lock:
            return self._alerts.get(alert_id)

    def save_results(self, alert_id: str, results: PipelineResults) -> bool:
        """
        Attach pipeline output to an existing alert. Returns True if the alert
        existed and was updated, False if the alert_id wasn't in the store.

        If False, the caller can decide whether to insert a new row (e.g. for
        free-text alerts that aren't pre-seeded). For the hackathon demo we
        only persist results for pre-seeded alerts, so False is fine to ignore.
        """
        with self._lock:
            alert = self._alerts.get(alert_id)
            if alert is None:
                return False
            alert.processed_at = datetime.now(timezone.utc).isoformat()
            alert.pipeline_results = results
            return True


# Module-level singleton. Every module that imports `store` gets the same instance.
store = AlertStore()
