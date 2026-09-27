"""
Prodapt AI Operations Center - shared configuration.

Every module in this project (LlamaIndex RAG, ADK services, LangGraph
orchestration, CrewAI, Streamlit UI) imports paths and settings from here
instead of hard-coding them, so the project can be pointed at a different
.env or data folder in one place.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env")

# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------
DATA_DIR = PROJECT_ROOT / "data"
DOCUMENTS_DIR = DATA_DIR / "documents"
VECTOR_INDEX_DIR = DATA_DIR / "vector_index"
DB_PATH = DATA_DIR / "telecom_ops.db"

SQL_DIR = PROJECT_ROOT / "sql"
SCHEMA_SQL_PATH = SQL_DIR / "01_schema.sql"
SEED_SQL_PATH = SQL_DIR / "02_seed_data.sql"

# --------------------------------------------------------------------------
# LLM / embedding configuration (LlamaIndex + CrewAI + LangGraph supervisor)
# --------------------------------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# --------------------------------------------------------------------------
# Google ADK configuration
# --------------------------------------------------------------------------
# Default routes ADK agents through OpenAI (via LiteLLM) so the project runs
# end-to-end with only OPENAI_API_KEY set. Set ADK_MODEL=gemini-2.0-flash and
# GOOGLE_API_KEY to use Gemini instead.
ADK_MODEL = os.getenv("ADK_MODEL", "openai/gpt-4o-mini")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

NETWORK_DIAGNOSTICS_PORT = int(os.getenv("NETWORK_DIAGNOSTICS_PORT", "8001"))
BILLING_RESOLUTION_PORT = int(os.getenv("BILLING_RESOLUTION_PORT", "8002"))

NETWORK_DIAGNOSTICS_AGENT_URL = os.getenv(
    "NETWORK_DIAGNOSTICS_AGENT_URL", f"http://localhost:{NETWORK_DIAGNOSTICS_PORT}"
)
BILLING_RESOLUTION_AGENT_URL = os.getenv(
    "BILLING_RESOLUTION_AGENT_URL", f"http://localhost:{BILLING_RESOLUTION_PORT}"
)

AGENT_CARD_PATH = "/.well-known/agent-card.json"

# --------------------------------------------------------------------------
# Business rules (mirrored from billing_disputes_policy.txt / 01_schema.sql)
# --------------------------------------------------------------------------
BILLING_AUTO_APPROVAL_LIMIT = 50.00


def get_adk_model():
    """
    Resolve the ADK_MODEL setting into whatever google.adk.agents.Agent(model=...)
    expects.

    - "provider/model" strings (e.g. "openai/gpt-4o-mini", "anthropic/claude-...")
      are wrapped with LiteLlm so ADK calls that provider instead of Gemini.
    - A bare model id (e.g. "gemini-2.0-flash") is passed straight through to
      ADK's native Gemini client, which requires GOOGLE_API_KEY.
    """
    model_name = ADK_MODEL
    if "/" in model_name:
        from google.adk.models.lite_llm import LiteLlm

        return LiteLlm(model=model_name)
    return model_name
