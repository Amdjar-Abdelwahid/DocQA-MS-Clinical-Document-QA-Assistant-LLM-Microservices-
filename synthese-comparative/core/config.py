# core/config.py
import os


def _env_bool(name: str, default: str = "true") -> bool:
    return os.getenv(name, default).lower() in ("1", "true", "yes", "y")


# URL du semantic indexer (microservice déjà existant)
SEMANTIC_INDEXER_URL: str = os.getenv(
    "SEMANTIC_INDEXER_URL",
    "http://semantic-indexer:8003"  # à adapter à ton docker-compose
)

# URL du microservice LLM-QA (pour appeler un vrai LLM)
LLM_QA_URL: str = os.getenv(
    "LLM_QA_URL",
    "http://llm-qa:8004"  # à adapter à ton docker-compose
)

# Flags pour activer/désactiver les FAKE
USE_FAKE_RETRIEVAL: bool = _env_bool("USE_FAKE_RETRIEVAL", "true")
USE_FAKE_LLM: bool = _env_bool("USE_FAKE_LLM", "true")
