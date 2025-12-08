# api/routes.py
from fastapi import APIRouter, HTTPException
from core.llm_client import LLMClient
from core.prompts import SINGLE_PATIENT_TEMPLATE, MULTI_PATIENT_TEMPLATE
from core.retrieval_client import RetrievalClient
from models.requests import PatientSummaryRequest, PatientComparisonRequest
from models.responses import (
    SinglePatientSummaryResponse,
    MultiPatientComparisonResponse,
    Section,
    SourceSnippet,
    ComparisonRow,
)

router = APIRouter()

# Create clients (in a real app you might inject them via dependencies)
llm_client = LLMClient()
retrieval_client = RetrievalClient()


@router.get("/status")
async def status():
    return {"status": "SyntheseComparative is running"}


@router.post(
    "/synthese/patient",
    response_model=SinglePatientSummaryResponse,
    summary="Generate a structured summary for a single patient",
)
async def generate_patient_summary(req: PatientSummaryRequest):
    # 1. Retrieve documents for that patient
    docs = await retrieval_client.get_patient_documents(
        patient_id=req.patient_id,
        from_date=req.from_date,
        to_date=req.to_date,
        focus=req.focus,
    )

    if not docs:
        raise HTTPException(status_code=404, detail="No documents found for this patient.")

    # 2. Build a single big string with all docs
    documents_str = "\n\n".join(
        f"[{d.get('doc_id', 'UNKNOWN')}]\n{d.get('text', '')}" for d in docs
    )

    # 3. Build the prompt
    prompt = SINGLE_PATIENT_TEMPLATE.format(
        patient_alias=f"PATIENT_{req.patient_id}",
        from_date=req.from_date or "N/A",
        to_date=req.to_date or "N/A",
        focus=req.focus or "général",
        documents=documents_str,
    )

    # 4. Call the (fake) LLM client
    summary_text = llm_client.summarize(prompt)

    # 5. Build the response object
    response = SinglePatientSummaryResponse(
        patient_alias=f"PATIENT_{req.patient_id}",
        time_range={"from": req.from_date, "to": req.to_date},
        sections=[Section(title="Synthèse clinique", content=summary_text)],
        key_points=[],  # TODO: later you can post-process to extract bullets
        sources=[
            SourceSnippet(
                doc_id=d.get("doc_id", "UNKNOWN"),
                snippet=d.get("text", "")[:300],
            )
            for d in docs[:5]
        ],
    )
    return response


@router.post(
    "/synthese/comparaison",
    response_model=MultiPatientComparisonResponse,
    summary="Generate a comparative summary between multiple patients",
)
async def generate_patient_comparison(req: PatientComparisonRequest):
    if len(req.patient_ids) < 2:
        raise HTTPException(status_code=400, detail="At least two patients are required.")

    documents_by_patient_str = ""
    all_sources = []

    # 1. Retrieve docs for each patient and build a big string
    for pid in req.patient_ids:
        docs = await retrieval_client.get_patient_documents(
            patient_id=pid,
            from_date=req.from_date,
            to_date=req.to_date,
            focus=req.focus,
        )

        documents_by_patient_str += f"\n\n=== PATIENT_{pid} ===\n"
        for d in docs:
            documents_by_patient_str += f"[{d.get('doc_id', 'UNKNOWN')}]\n{d.get('text', '')}\n"

        for d in docs[:3]:
            all_sources.append(
                SourceSnippet(
                    doc_id=d.get("doc_id", "UNKNOWN"),
                    snippet=d.get("text", "")[:300],
                )
            )

    # 2. Build the prompt
    prompt = MULTI_PATIENT_TEMPLATE.format(
        patients=[f"PATIENT_{p}" for p in req.patient_ids],
        from_date=req.from_date or "N/A",
        to_date=req.to_date or "N/A",
        focus=req.focus or "général",
        documents_by_patient=documents_by_patient_str,
    )

    # 3. Call the LLM client
    summary_text = llm_client.summarize(prompt)

    # 4. For the moment, create a simple placeholder comparison table
    comparison_table = [
        ComparisonRow(
            dimension="Exemple de dimension",
            patient_1="Informations principales patient 1",
            patient_2="Informations principales patient 2",
        )
    ]

    response = MultiPatientComparisonResponse(
        patients=[f"PATIENT_{p}" for p in req.patient_ids],
        time_range={"from": req.from_date, "to": req.to_date},
        summary=summary_text,
        comparison_table=comparison_table,
        key_risks=[],
        sources=all_sources[:10],
    )
    return response
