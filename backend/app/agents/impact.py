import logging
import re
from backend.app.models.schemas import ScoutOutput, InvestigatorOutput, ImpactOutput
from backend.app.agents.prompts import IMPACT_PROMPT
from backend.app.agents.router import call_llm
from backend.app.agents.base import call_and_validate_with_retry, parse_and_validate
from backend.app.tools.asset_lookup import lookup_asset

logger = logging.getLogger("decision_platform.impact")

# Match any 2-5 digit port number
PORT_REGEX = re.compile(r'\b(\d{2,5})\b')
IP_REGEX = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')

# Common version numbers to skip when extracting ports
_VERSION_NOISE = {2, 4, 80}  # v4.2, HTTP/2, etc.

# Fallback if LLM fails twice — keeps the pipeline running
_IMPACT_FALLBACK = ImpactOutput(
    severity="MEDIUM",
    affected_asset="Unknown Asset",
    potential_damage="Unable to assess impact automatically. Manual review required.",
)


def _find_port_in_text(text: str) -> int:
    """
    Find a plausible port number in a text string.
    Strategy:
      1. Look for explicit 'port N' or 'on port N' patterns first (high confidence)
      2. Fall back to any standalone 2-5 digit number (low confidence)
    """
    # Strategy 1: explicit port mention (much more reliable)
    explicit_port_patterns = [
        r'(?:on\s+)?port\s+(\d{2,5})\b',     # "port 8080" or "on port 8080"
        r':(\d{2,5})\b',                     # "10.0.0.150:8080" style
        r'@port\s*(\d{2,5})\b',              # "@port 6379"
    ]
    for pattern in explicit_port_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            port = int(match.group(1))
            if 1 <= port <= 65535:
                return port

    # Strategy 2: any standalone 2-5 digit number (fallback)
    for match in PORT_REGEX.finditer(text):
        port = int(match.group(1))
        if not (1 <= port <= 65535):
            continue
        if port in _VERSION_NOISE:
            continue
        # Skip if surrounded by dots (version like "v4.2")
        start, end = match.span()
        if start > 0 and text[start - 1] == '.':
            continue
        if end < len(text) and text[end] == '.':
            continue
        return port
    return 0


def _extract_port(scout_output: ScoutOutput, raw_alert: str = "") -> int:
    """
    Extract port number with a fallback chain:
      1. Try Scout's target field
      2. Try Scout's action field
      3. Try the original raw alert text
      4. Fall back to 8080 only as last resort
    """
    for text in [scout_output.target, scout_output.action]:
        port = _find_port_in_text(text)
        if port:
            return port
    if raw_alert:
        port = _find_port_in_text(raw_alert)
        if port:
            logger.info(f"Impact Agent: Port recovered from raw alert: {port}")
            return port
    return 8080  # last-resort fallback


def _extract_ip(scout_output: ScoutOutput, raw_alert: str = "") -> str:
    """
    Extract IPv4 with fallback chain:
      1. Try Scout's target field
      2. Try Scout's action field
      3. Try the original raw alert text
    """
    for text in [scout_output.target, scout_output.action]:
        match = IP_REGEX.search(text)
        if match:
            return match.group(0)
    if raw_alert:
        match = IP_REGEX.search(raw_alert)
        if match:
            logger.info(f"Impact Agent: IP recovered from raw alert: {match.group(0)}")
            return match.group(0)
    return "unknown"


def _build_asset_context(asset_record) -> str:
    """Format the asset record as grounding context for the LLM."""
    if asset_record:
        return (
            f"- Asset Name: {asset_record.asset_name}\n"
            f"- Asset IP: {asset_record.ip}\n"
            f"- Asset Port: {asset_record.port}\n"
            f"- Business Segment: {asset_record.business_segment}\n"
            f"- Record Count: {asset_record.record_count}\n"
            f"- Data Sensitivity: {asset_record.data_sensitivity}"
        )
    return "- No matching asset found in inventory. Use 'Unknown Asset' as the affected_asset name."


def assess_impact(
    scout_output: ScoutOutput,
    investigator_output: InvestigatorOutput,
    raw_alert: str = "",
) -> ImpactOutput:
    """
    Impact Agent process:
    1. Extract target IP and port from ScoutOutput (with raw_alert as fallback).
    2. Invoke lookup_asset(ip, port) to get ground truth from inventory.
    3. Format IMPACT_PROMPT with diagnosis + grounded asset context.
    4. Calls call_llm() with retry + fallback.
    5. Returns validated ImpactOutput.
    """
    logger.info("Impact Agent: Starting impact assessment...")

    ip = _extract_ip(scout_output, raw_alert)
    port = _extract_port(scout_output, raw_alert)
    logger.info(f"Impact Agent: Querying asset inventory with IP={ip}, Port={port}")

    asset_record = lookup_asset(ip, port)
    asset_context = _build_asset_context(asset_record)

    prompt = (
        IMPACT_PROMPT
        .replace("{diagnosis}", investigator_output.diagnosis)
        .replace("{confidence_score}", str(investigator_output.confidence_score))
        .replace("{asset_context}", asset_context)
    )

    try:
        return call_and_validate_with_retry(
            prompt=prompt,
            agent_name="ImpactAgent",
            schema_class=ImpactOutput,
            llm_caller=call_llm,
            fallback=_IMPACT_FALLBACK,
        )
    except Exception as e:
        logger.error(f"Impact Agent: LLM call failed: {e}")
        raise RuntimeError(f"Impact Agent LLM call failed: {e}")