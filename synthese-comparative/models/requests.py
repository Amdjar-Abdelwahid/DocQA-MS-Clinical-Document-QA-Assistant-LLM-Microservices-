# models/requests.py
from pydantic import BaseModel
from typing import List, Optional


class PatientSummaryRequest(BaseModel):
    """Request body for generating a single-patient summary."""
    patient_id: str
    from_date: Optional[str] = None  # ISO format "YYYY-MM-DD"
    to_date: Optional[str] = None
    focus: Optional[str] = None      # e.g. "anticoagulant", "diabète"
    language: str = "fr"


class PatientComparisonRequest(BaseModel):
    """Request body for generating a multi-patient comparison."""
    patient_ids: List[str]
    from_date: Optional[str] = None
    to_date: Optional[str] = None
    focus: Optional[str] = None
    language: str = "fr"
