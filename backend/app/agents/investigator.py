import logging
import re
from backend.app.models.schemas import ScoutOutput, InvestigatorOutput
from backend.app.agents.prompts import INVESTIGATOR_PROMPT
from backend.app.agents.router import call_llm
from backend.app.agents.base import call_and_validate_with_retry
from backend.app.tools.cve_lookup import lookup_cve

logger = logging.getLogger("decision_platform.investigator")

# Fallback if LLM fails twice — keeps the pipeline running
_INVESTIGATOR_FALLBACK = InvestigatorOutput(
    diagnosis="Unable to determine specific vulnerability. Manual investigation required.",
    confidence_score=50,
)


def _extract_cve_id(text: str) -> str:
    """Extract a CVE-ID (e.g., CVE-2026-0001) from a string if present."""
    match = re.search(r'CVE-\d{4}-\d{4,7}', text, re.IGNORECASE)
    return match.group(0) if match else ""


def _build_cve_context(scout_output: ScoutOutput) -> str:
    """
    Build a grounding string for the LLM based on the local CVE database.
    Strategy:
      1. If a CVE-ID is present in the Scout output, look it up directly.
      2. Otherwise, try keyword lookup using the software name extracted from target/action.
      3. If a CVE record is found, format it as structured context.
      4. If nothing is found, return a 'no match' note so the LLM still gets a clear signal.
    """
    combined = f"{scout_output.target} {scout_output.action}"

    # Strategy 1: direct CVE-ID lookup
    cve_id = _extract_cve_id(combined)
    cve_record = lookup_cve(cve_id) if cve_id else None

    # Strategy 2: keyword fallback — try common software tokens
    if not cve_record:
        candidates = re.findall(r'[A-Za-z][A-Za-z0-9._-]+', combined)
        for token in candidates:
            if token.lower() in {"on", "via", "from", "port", "ip", "the", "and", "to", "attempt", "access"}:
                continue
            cve_record = lookup_cve(token)
            if cve_record:
                break

    if cve_record:
        return (
            f"- CVE ID: {cve_record.id}\n"
            f"- Description: {cve_record.description}\n"
            f"- CVSS Score: {cve_record.cvss_score}\n"
            f"- Severity: {cve_record.severity}"
        )
    return "- No matching CVE found in local database. Diagnose based on the Scout output alone. Return valid JSON."


def investigate_scout_output(scout_output: ScoutOutput) -> InvestigatorOutput:
    """
    Investigator Agent process:
    1. Receives ScoutOutput.
    2. Queries local CVE database for a matching vulnerability (the 'second wow moment').
    3. Formats INVESTIGATOR_PROMPT with ScoutOutput fields + grounded CVE context.
    4. Calls call_llm() with retry + fallback.
    5. Caps confidence at 95 (Qwen 0.8B ignores prompt rules).
    6. Returns validated InvestigatorOutput.
    """
    logger.info("Investigator Agent: Starting investigation on scout output...")

    cve_context = _build_cve_context(scout_output)
    logger.info(f"Investigator Agent: CVE context grounded -> {cve_context.splitlines()[0]}")

    prompt = (
        INVESTIGATOR_PROMPT
        .replace("{target}", scout_output.target)
        .replace("{attacker_ip}", scout_output.attacker_ip)
        .replace("{action}", scout_output.action)
        .replace("{cve_context}", cve_context)
    )

    try:
        result = call_and_validate_with_retry(
            prompt=prompt,
            agent_name="InvestigatorAgent",
            schema_class=InvestigatorOutput,
            llm_caller=call_llm,
            fallback=_INVESTIGATOR_FALLBACK,
        )
    except Exception as e:
        logger.error(f"Investigator Agent: LLM call failed: {e}")
        raise RuntimeError(f"Investigator Agent LLM call failed: {e}")

    # Qwen 0.8B ignores the "never 100" rule in the prompt — enforce it in code
    if result.confidence_score > 95:
        logger.info(f"Investigator Agent: Capping confidence {result.confidence_score} -> 95")
        result = result.model_copy(update={"confidence_score": 95})

    return result