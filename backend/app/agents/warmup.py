import logging
import threading
import httpx
from backend.app.config import settings

logger = logging.getLogger("decision_platform.warmup")

# How long Ollama keeps the big model resident after each touch. Generous
# on purpose: must outlast the Impact -> Commander gap, and ideally the
# gap between one demo alert and the next.
BIG_MODEL_KEEP_ALIVE = "30m"

# Agents that need the big model — kept here so router.py and sse.py
# both reference one source of truth.
BIG_MODEL_AGENTS = {"ImpactAgent", "CommanderAgent"}


class ModelWarmer:
    """One instance per pipeline run. start() kicks off the background
    load; wait() blocks (briefly, with a cap) until it's ready."""

    def __init__(self, model: str):
        self.model = model
        self.ready = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> "ModelWarmer":
        self._thread = threading.Thread(target=self._warm, daemon=True)
        self._thread.start()
        return self

    def _warm(self):
        endpoint = f"{settings.OLLAMA_URL.rstrip('/')}/api/generate"
        try:
            logger.info(f"[warmup] pre-loading {self.model}...")
            with httpx.Client() as client:
                # Empty prompt -> Ollama loads the model into memory and
                # returns as soon as it's resident, without generating
                # any tokens. This is the standard Ollama warm-up call.
                client.post(
                    endpoint,
                    json={
                        "model": self.model,
                        "prompt": "",
                        "stream": False,
                        "keep_alive": BIG_MODEL_KEEP_ALIVE,
                    },
                    timeout=60.0,  # generous — not on the user-facing clock
                )
            logger.info(f"[warmup] {self.model} is warm")
        except Exception as e:
            # Never raise from here. Worst case, Impact/Commander's own
            # call_llm() hits a cold model and pays the load cost itself,
            # or falls back to Groq — exactly what already happens today.
            logger.warning(f"[warmup] failed to pre-load {self.model}: {e}")
        finally:
            self.ready.set()

    def wait(self, timeout: float) -> bool:
        """Block up to `timeout` seconds. Returns True if warm-up finished
        in time (success OR failure — failure also sets ready, see above),
        False if it's still in flight."""
        return self.ready.wait(timeout=timeout)


# --- Module-level "current run" registry ------------------------------
# Lets router.call_llm() reach the active warmer without threading a new
# parameter through call_and_validate_with_retry / every agent function.
_current: ModelWarmer | None = None


def start_new_run() -> ModelWarmer:
    """Call once per pipeline run, as early as possible (sse.py does this
    right at pipeline_start, before Scout)."""
    global _current
    _current = ModelWarmer(settings.OLLAMA_MODEL).start()
    return _current


def get_current() -> ModelWarmer | None:
    return _current


def warm_at_startup() -> ModelWarmer:
    """Call once when the FastAPI process boots (main.py), so the very
    first demo alert doesn't eat a cold-load penalty live in front of
    judges. Independent of any pipeline run."""
    return ModelWarmer(settings.OLLAMA_MODEL).start()
