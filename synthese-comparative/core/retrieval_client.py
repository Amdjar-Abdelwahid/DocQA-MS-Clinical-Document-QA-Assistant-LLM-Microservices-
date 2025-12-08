# core/retrieval_client.py
from typing import List, Dict, Optional
import httpx

from core.config import SEMANTIC_INDEXER_URL, USE_FAKE_RETRIEVAL


class RetrievalClient:
    """
    Client for retrieving clinical snippets.
    - If USE_FAKE_RETRIEVAL = true  -> returns hard-coded fake data.
    - If USE_FAKE_RETRIEVAL = false -> calls the real semantic-indexer microservice.
    """

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or SEMANTIC_INDEXER_URL

    async def get_patient_documents(
        self,
        patient_id: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        focus: Optional[str] = None,
    ) -> List[Dict]:
        if USE_FAKE_RETRIEVAL:
            return self._get_fake_documents(patient_id, from_date, to_date, focus)
        return await self._get_real_documents(patient_id, from_date, to_date, focus)

    # ---------- FAKE MODE ----------

    def _get_fake_documents(
        self,
        patient_id: str,
        from_date: Optional[str],
        to_date: Optional[str],
        focus: Optional[str],
    ) -> List[Dict]:
        """Used only for local dev when USE_FAKE_RETRIEVAL=true."""
        fake_text_1 = (
            f"Compte-rendu clinique pour le patient {patient_id}. "
            f"Période: {from_date} -> {to_date}. "
            f"Focus: {focus or 'général'}. "
            "Le patient est suivi pour un traitement anticoagulant avec surveillance régulière de l'INR."
        )

        fake_text_2 = (
            "Événement clinique important : ajustement de la dose après épisode "
            "hémorragique mineur. Aucun nouvel événement majeur signalé par la suite."
        )

        return [
            {"doc_id": f"FAKE-DOC-{patient_id}-1", "text": fake_text_1},
            {"doc_id": f"FAKE-DOC-{patient_id}-2", "text": fake_text_2},
        ]

    # ---------- REAL MODE ----------

    async def _get_real_documents(
        self,
        patient_id: str,
        from_date: Optional[str],
        to_date: Optional[str],
        focus: Optional[str],
    ) -> List[Dict]:
        """
        Calls the real semantic-indexer microservice.

        ⚠️ IMPORTANT:
        - Adapte le chemin "/api/search/patient-snippets" à ton vrai MS semantic-indexer.
        - Adapte aussi les noms de paramètres si besoin.

        Exemple d'API attendue côté semantic-indexer:
            GET /api/search/patient-snippets?patient_id=P123&from_date=...&to_date=...&focus=...

        Réponse JSON attendue:
            [
              {"doc_id": "DOC-123", "text": "..."},
              {"doc_id": "DOC-456", "text": "..."}
            ]
        """
        params = {
            "patient_id": patient_id,
            "from_date": from_date,
            "to_date": to_date,
            "focus": focus,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(f"{self.base_url}/api/search/patient-snippets", params=params)
            resp.raise_for_status()
            return resp.json()
