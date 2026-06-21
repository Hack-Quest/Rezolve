import logging
from backend.app.models.schemas import ScoutOutput
from backend.app.agents.prompts import SCOUT_PROMPT
from backend.app.agents.router import call_llm
from backend.app.agents.base import call_and_validate_with_retry

logger = logging.getLogger("decision_platform.scout")

# Fallback if LLM fails twice — keeps the pipeline running
_SCOUT_FALLBACK = ScoutOutput(
    target="unknown",
    attacker_ip="unknown",
    action="Security incident",
)


def scout_alert(raw_alert: str) -> ScoutOutput:
    """
    Scout Agent process:
    1. Injects raw alert into SCOUT_PROMPT.
    2. Calls call_llm() with retry + fallback.
    3. Returns validated ScoutOutput.
    """
    logger.info("Scout Agent: Starting processing of raw alert...")
    prompt = SCOUT_PROMPT.replace("{raw_alert}", raw_alert)

    try:
        return call_and_validate_with_retry(
            prompt=prompt,
            agent_name="ScoutAgent",
            schema_class=ScoutOutput,
            llm_caller=call_llm,
            fallback=_SCOUT_FALLBACK,
        )
    except Exception as e:
        logger.error(f"Scout Agent: LLM call failed: {e}")
        raise RuntimeError(f"Scout Agent LLM call failed: {e}")