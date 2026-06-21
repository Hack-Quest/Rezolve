import logging
import httpx
from backend.app.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("decision_platform.router")

# Tiered Model Mappings
OLLAMA_MODEL_MAPPING = {
    "ScoutAgent": "qwen3.5:0.8b",
    "InvestigatorAgent": "qwen3.5:0.8b",
    "ImpactAgent": "llama3:8b",
    "CommanderAgent": "llama3:8b"
}

GROQ_MODEL_MAPPING = {
    "ScoutAgent": "llama-3.1-8b-instant",
    "InvestigatorAgent": "llama-3.1-8b-instant",
    "ImpactAgent": "llama-3.3-70b-versatile",
    "CommanderAgent": "llama-3.3-70b-versatile"
}

def call_llm(prompt: str, agent_name: str) -> str:
    """
    Calls Ollama first, with a hard timeout of 8 seconds.
    If Ollama fails or times out, falls back to Groq (15 second timeout).
    Uses tiered model mapping based on the agent's name.
    Returns only the generated text response.
    """
    logger.info(f"[{agent_name}] Initiating LLM call...")
    
    # Select appropriate models for this agent
    ollama_model = OLLAMA_MODEL_MAPPING.get(agent_name, settings.OLLAMA_MODEL)
    groq_model = GROQ_MODEL_MAPPING.get(agent_name, settings.GROQ_MODEL)
    
    # 1. Attempt Ollama
    ollama_endpoint = f"{settings.OLLAMA_URL.rstrip('/')}/api/generate"
    try:
        logger.info(f"[{agent_name}] Trying Ollama at {ollama_endpoint} (Model: {ollama_model})")
        payload = {
            "model": ollama_model,
            "prompt": prompt,
            "stream": False,
            "think": False,
            "format": "json"
        }
        
        with httpx.Client() as client:
            response = client.post(
                ollama_endpoint,
                json=payload,
                timeout=10.0  # Bail fast — at 9 tok/s, anything over 10s means Ollama is struggling. Fall back to Groq.
            )
            response.raise_for_status()
            result = response.json()
            generated_text = result.get("response", "")
            
            logger.info(f"[{agent_name}] Successfully retrieved response from Ollama")
            return generated_text
            
    except Exception as e:
        logger.warning(f"[{agent_name}] Ollama attempt failed or timed out: {type(e).__name__}: {e}. Falling back to Groq...")

    # 2. Fallback to Groq
    if not settings.GROQ_API_KEY:
        raise RuntimeError(
            f"[{agent_name}] Ollama failed and Groq cannot be used because GROQ_API_KEY is not set."
        )

    try:
        logger.info(f"[{agent_name}] Trying Groq at {settings.GROQ_API_URL} (Model: {groq_model})")
        headers = {
            "Authorization": f"Bearer {settings.GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": groq_model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.0,
            "stream": False
        }
        
        with httpx.Client() as client:
            response = client.post(
                settings.GROQ_API_URL,
                json=payload,
                headers=headers,
                timeout=15.0  # Cloud is fast and reliable — 15s is generous for Impact/Commander on Llama 3 70B
            )
            response.raise_for_status()
            result = response.json()
            
            choices = result.get("choices", [])
            if not choices:
                raise ValueError("Groq response did not contain 'choices'.")
            
            generated_text = choices[0].get("message", {}).get("content", "")
            logger.info(f"[{agent_name}] Successfully retrieved response from Groq")
            return generated_text
            
    except Exception as e:
        logger.error(f"[{agent_name}] Groq fallback also failed: {type(e).__name__}: {e}")
        raise RuntimeError(
            f"Both LLM providers failed. Ollama failed/timed out, and Groq fallback encountered: {e}"
        )