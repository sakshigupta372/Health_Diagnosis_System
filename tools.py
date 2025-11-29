import os
from typing import Dict, List, Optional
import requests
from crewai.tools import tool
from .utils.logging import get_logger
from .config import GUIDELINES_API_URL, GUIDELINES_API_KEY
logger = get_logger(__name__)


# Medical knowledge tools
@tool("medical_knowledge_search")
def medical_knowledge_search(query: str = "", **kwargs) -> str:
    """Search medical knowledge databases for conditions and treatments (stub, resilient).

    - Accepts empty/missing queries and unexpected kwargs.
    - Coerces non-string inputs to string.
    - Always returns a concise, safe stubbed response to avoid agent failure.
    """
    try:
        q = str(query).strip() if query is not None else ""
        if not q:
            q = "presented symptoms"
        logger.info("Searching medical knowledge for query: %s", q)
        return (
            f"Knowledge summary for {q}: consider common and serious differentials; correlate with vitals, "
            f"onset, red flags (fever, neuro deficits), and patient comorbidities. Use evidence-based "
            f"sources and confirm with clinical guidelines."
        )
    except Exception as e:
        logger.exception("Knowledge search failed, returning safe fallback: %s", e)
        return (
            "Knowledge summary: review common causes and rule out emergencies; validate with guidelines and "
            "clinical judgment."
        )


# Drug interaction tool
@tool("drug_interaction_check")
def drug_interaction_check(medications: List[str]) -> Dict:
    """Check for drug interactions and contraindications (stub)."""
    logger.info("Checking drug interactions for: %s", medications)
    warnings = []
    if (
        len(medications) >= 2
        and "ibuprofen" in [m.lower() for m in medications]
        and "aspirin" in [m.lower() for m in medications]
    ):
        warnings.append(
            "Caution combining ibuprofen and aspirin due to antiplatelet effect interference."
        )
    return {"warnings": warnings, "severity": "low" if not warnings else "moderate"}


@tool("clinical_guidelines_search")
def clinical_guidelines_search(condition: str = "", **kwargs) -> str:
    """Retrieve clinical guidelines for specific conditions (stub, resilient).

    This function is tolerant to:
    - Empty or missing condition values
    - Calls that pass unexpected extra fields
    - Non-string inputs convertible to string

    It always returns a short, safe stubbed guideline summary so agents do not fail.
    """
    try:
        # Accept non-string inputs safely
        cond = str(condition).strip() if condition is not None else ""
        if not cond:
            cond = "the presented symptoms"
        logger.info("Retrieving clinical guidelines for: %s", cond)

        # If external API configured, try it first
        if GUIDELINES_API_URL and GUIDELINES_API_KEY:
            try:
                resp = requests.get(
                    GUIDELINES_API_URL.rstrip("/") + "/guidelines",
                    params={"q": cond},
                    headers={"Authorization": f"Bearer {GUIDELINES_API_KEY}"},
                    timeout=10,
                )
                if resp.ok:
                    data = resp.json()
                    # Expecting data like {"summary": "...", "sources": [...]}
                    summary = data.get("summary")
                    if summary:
                        return f"Guideline summary for {cond}: {summary}"
                else:
                    logger.warning("Guidelines API non-OK status: %s %s", resp.status_code, resp.text)
            except Exception as api_err:
                logger.warning("Guidelines API call failed, using fallback. Error: %s", api_err)

        # Fallback stub
        return (
            f"Guideline summary for {cond}: use evidence-based protocols; consider red flags, "
            f"patient comorbidities (e.g., hypertension), and follow-up within appropriate timelines."
        )
    except Exception as e:
        logger.exception("Guidelines lookup failed, returning safe fallback: %s", e)
        return (
            "Guideline summary: follow standard supportive care; check for red flags and ensure timely "
            "follow-up."
        )


# Healthcare system integration
@tool("electronic_health_record_access")
def electronic_health_record_access(patient_id: str) -> Dict:
    """Access patient EHR data (with proper authorization) (stub)."""
    logger.info("Accessing EHR for patient: %s", patient_id)
    return {
        "patient_id": patient_id,
        "allergies": ["penicillin"],
        "chronic_conditions": ["hypertension"],
        "medications": ["lisinopril"],
        "family_history": ["diabetes"],
    }


@tool("appointment_scheduling")
def appointment_scheduling(specialty: str, urgency: str) -> Dict:
    """Schedule appointments with healthcare providers (stub)."""
    logger.info("Scheduling appointment for specialty=%s urgency=%s", specialty, urgency)
    return {
        "specialty": specialty,
        "urgency": urgency,
        "scheduled": True,
        "date": "2025-10-05",
        "notes": "Stubbed appointment scheduled via demo scheduler.",
    }
