import logging
from backend.app.models.schemas import InvestigatorOutput, ImpactOutput, CommanderOutput
from backend.app.agents.prompts import COMMANDER_PROMPT
from backend.app.agents.router import call_llm
from backend.app.agents.base import call_and_validate_with_retry
from backend.app.tools.playbook_lookup import lookup_playbook

logger = logging.getLogger("decision_platform.commander")

# Fallback if LLM fails twice — keeps the pipeline running
_COMMANDER_FALLBACK = CommanderOutput(
    summary_headline="INCIDENT DETECTED — Manual Review Required",
    recommended_actions=[
        "Investigate the affected system manually.",
        "Check system and application logs for indicators of compromise.",
        "Alert the on-call security engineer for verification.",
    ],
)


def _build_playbook_context(playbook) -> str:
    """Format the playbook as grounding context for the LLM."""
    if playbook:
        lines = [f"Playbook ID: {playbook.playbook_id}"]
        for i, step in enumerate(playbook.steps, 1):
            lines.append(f"{i}. {step}")
        return "\n".join(lines)
    return "No playbook steps available for this severity."


def generate_command(investigator_output: InvestigatorOutput, impact_output: ImpactOutput) -> CommanderOutput:
    """
    Commander Agent process:
    1. Receives InvestigatorOutput and ImpactOutput.
    2. Invokes lookup_playbook(severity) to get grounded playbook steps.
    3. Formats COMMANDER_PROMPT with incident details + grounded playbook context.
    4. Calls call_llm() with retry + fallback.
    5. Returns validated CommanderOutput.
    """
    logger.info("Commander Agent: Starting command generation...")

    severity = impact_output.severity
    logger.info(f"Commander Agent: Querying playbook for severity={severity}")
    playbook = lookup_playbook(severity)
    playbook_context = _build_playbook_context(playbook)

    prompt = (
        COMMANDER_PROMPT
        .replace("{diagnosis}", investigator_output.diagnosis)
        .replace("{severity}", impact_output.severity)
        .replace("{affected_asset}", impact_output.affected_asset)
        .replace("{potential_damage}", impact_output.potential_damage)
        .replace("{playbook_context}", playbook_context)
    )

    try:
        return call_and_validate_with_retry(
            prompt=prompt,
            agent_name="CommanderAgent",
            schema_class=CommanderOutput,
            llm_caller=call_llm,
            fallback=_COMMANDER_FALLBACK,
        )
    except Exception as e:
        logger.error(f"Commander Agent: LLM call failed: {e}")
        raise RuntimeError(f"Commander Agent LLM call failed: {e}")