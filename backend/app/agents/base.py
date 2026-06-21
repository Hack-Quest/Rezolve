import json
import logging
import re
from pydantic import BaseModel, ValidationError
from typing import Type, TypeVar, Optional, Callable

T = TypeVar("T", bound=BaseModel)

logger = logging.getLogger("decision_platform.agents.base")


def clean_json_response(response_text: str) -> str:
    """
    Cleans markdown code blocks (e.g. ```json ... ```) from the LLM response text.
    """
    cleaned = response_text.strip()
    if cleaned.startswith("```"):
        match = re.search(r"^```(?:json)?\n?(.*?)\n?```$", cleaned, re.DOTALL | re.IGNORECASE)
        if match:
            cleaned = match.group(1).strip()
    return cleaned


def parse_and_validate(response_text: str, schema_class: Type[T], agent_name: str) -> T:
    """
    Cleans, parses, and validates the LLM JSON response against a target Pydantic model.
    Raises ValueError if JSON is malformed or validation fails.
    """
    cleaned_text = clean_json_response(response_text)

    try:
        data = json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        logger.error(f"{agent_name}: JSON decode error: {e}. Raw response: {response_text}")
        raise ValueError(f"{agent_name} received malformed JSON: {e}")

    try:
        validated_output = schema_class(**data)
        logger.info(f"{agent_name}: Successfully parsed and validated {schema_class.__name__}.")
        return validated_output
    except ValidationError as e:
        logger.error(f"{agent_name}: Pydantic validation failed: {e}. Parsed data: {data}")
        raise ValueError(f"{agent_name} validation failed: {e}")


def call_and_validate_with_retry(
    prompt: str,
    agent_name: str,
    schema_class: Type[T],
    llm_caller: Callable[[str, str], str],
    max_retries: int = 1,
    fallback: Optional[T] = None,
) -> T:
    """
    Call the LLM, validate the response, and retry once with a stricter prompt if validation fails.
    If all attempts fail and a fallback is provided, return the fallback (keeps the demo alive).
    Otherwise, raise the last error.

    Usage from an agent:
        return call_and_validate_with_retry(
            prompt=prompt,
            agent_name="InvestigatorAgent",
            schema_class=InvestigatorOutput,
            llm_caller=call_llm,
            fallback=InvestigatorOutput(diagnosis="...", confidence_score=50),
        )
    """
    current_prompt = prompt
    last_error = None

    for attempt in range(max_retries + 1):
        try:
            response_text = llm_caller(current_prompt, agent_name)
            return parse_and_validate(response_text, schema_class, agent_name)
        except (ValueError, ValidationError) as e:
            last_error = e
            if attempt < max_retries:
                logger.warning(
                    f"{agent_name}: attempt {attempt + 1} failed ({type(e).__name__}). "
                    f"Retrying with corrective prompt..."
                )
                current_prompt = (
                    "Your previous response was invalid JSON or did not match the schema. "
                    "Return ONLY a valid JSON object. No markdown. No explanation. "
                    "No text before or after the JSON. Just the JSON object.\n\n"
                    f"Original task:\n{prompt}"
                )
            else:
                logger.error(f"{agent_name}: all {max_retries + 1} attempts failed.")

    if fallback is not None:
        logger.warning(f"{agent_name}: using fallback response after {max_retries + 1} failures.")
        return fallback

    raise ValueError(
        f"{agent_name} failed after {max_retries + 1} attempts. Last error: {last_error}"
    )