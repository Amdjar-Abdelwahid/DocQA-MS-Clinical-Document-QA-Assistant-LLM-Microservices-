# core/llm_client.py
from typing import Optional
import httpx

from core.config import LLM_QA_URL, USE_FAKE_LLM


class LLMClient:
    """
    LLM client with two modes:
    - FAKE mode: just truncates the prompt (for local dev).
    - REAL mode: calls the llm-qa microservice to get a proper summary.
    """

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or LLM_QA_URL

    def summarize(self, prompt: str, max_chars: int = 1200) -> str:
        if USE_FAKE_LLM:
            return self._summarize_fake(prompt, max_chars)
        return self._summarize_remote(prompt)

    # ---------- FAKE MODE ----------

    @staticmethod
    def _summarize_fake(prompt: str, max_chars: int) -> str:
        """Simple fake summarization by truncating the prompt."""
        if len(prompt) <= max_chars:
            return prompt
        return prompt[-max_chars:]

    # ---------- REAL MODE ----------

    def _call_llm_qa_sync(self, prompt: str) -> str:
        """
        Synchronous call to llm-qa microservice.

        ⚠️ IMPORTANT:
        - Adapte l'endpoint "/api/llm/summarize" au vrai endpoint de ton MS llm-qa.
        - Adapte aussi le body/response selon ton API.

        Exemple d'API attendue côté llm-qa:
            POST /api/llm/summarize
            body: {"prompt": "<texte>"}
            response: {"summary": "<résumé>"}
        """
        payload = {"prompt": prompt}

        # httpx en mode sync car la route FastAPI est async et on veut simplifier.
        with httpx.Client(timeout=60.0) as client:
            resp = client.post(f"{self.base_url}/api/llm/summarize", json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data.get("summary", "")

    def _summarize_remote(self, prompt: str) -> str:
        try:
            summary = self._call_llm_qa_sync(prompt)
            if not summary:
                # fallback si la réponse est vide
                return self._summarize_fake(prompt, 1200)
            return summary
        except Exception as exc:
            # En cas de problème réseau, on ne casse pas le MS: fallback fake
            return self._summarize_fake(prompt, 1200)
