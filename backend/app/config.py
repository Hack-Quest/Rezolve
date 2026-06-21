import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file. We search for it in current directory, parent directory, and grandparent directory to be robust.
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)
load_dotenv()  # fallback to standard search

class Settings:
    # Ollama Configuration
    OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
    
    # Groq Configuration
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_API_URL: str = os.getenv("GROQ_API_URL", "https://api.groq.com/openai/v1/chat/completions")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

settings = Settings()
