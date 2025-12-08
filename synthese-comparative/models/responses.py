# models/responses.py
from pydantic import BaseModel
from typing import List, Optional


class SourceSnippet(BaseModel):
    doc_id: str
    snippet: str


class Section(BaseModel):
    title: str
    content: str


class SinglePatientSummaryResponse(BaseModel):
    type: str = "single_patient_summary"
    patient_alias: str
    time_range: Optional[dict]
    sections: List[Section]
    key_points: List[str]
    sources: List[SourceSnippet]


class ComparisonRow(BaseModel):
    dimension: str
    patient_1: str
    patient_2: str


class MultiPatientComparisonResponse(BaseModel):
    type: str = "multi_patient_comparison"
    patients: List[str]
    time_range: Optional[dict]
    summary: str
    comparison_table: List[ComparisonRow]
    key_risks: List[str]
    sources: List[SourceSnippet]
