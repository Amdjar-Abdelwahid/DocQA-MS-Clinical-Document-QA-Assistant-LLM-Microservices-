# core/prompts.py

SINGLE_PATIENT_TEMPLATE = """
You are a medical assistant. Summarize the following clinical history
for ONE anonymized patient.

Context:
- Patient alias: {patient_alias}
- Time window: {from_date} to {to_date}
- Clinical focus: {focus}

Clinical notes:
{documents}

Task:
Produce a structured summary in FRENCH with sections:
1. Contexte général
2. Focus clinique ({focus})
3. Événements clés
4. Points de vigilance

Return ONLY the summary text (no extra comments, no JSON).
"""


MULTI_PATIENT_TEMPLATE = """
You are a medical assistant. Compare the clinical histories of
MULTIPLE anonymized patients.

Context:
- Patient aliases: {patients}
- Time window: {from_date} to {to_date}
- Clinical focus: {focus}

Clinical notes by patient:
{documents_by_patient}

Task:
In FRENCH, produce:
1. A global comparative summary
2. The main differences between patients (by dimensions: traitement, événements, risques...)
3. The key risk points for each patient

Return ONLY the final text (no extra comments, no JSON).
"""
