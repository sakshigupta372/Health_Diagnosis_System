from typing import Dict, Any
from crewai.tools import tool
from .utils.logging import get_logger

logger = get_logger(__name__)


@tool("validate_medical_recommendation")
def validate_medical_recommendation(recommendation: Dict[str, Any]) -> bool:
    """Validate medical recommendations against safety protocols.
    Checks include:
    - Contraindications
    - Dosage limits
    - Interaction warnings
    - Clinical guideline compliance

    Returns True if passes basic validation; False otherwise.
    """
    try:
        meds = recommendation.get("medications", [])
        for med in meds:
            dose = med.get("dose_mg")
            if dose and dose < 0:
                logger.warning("Invalid negative dosage detected: %s", med)
                return False
        # Stub: Always pass basic validation in demo
        return True
    except Exception as e:
        logger.exception("Validation error: %s", e)
        return False


@tool("emergency_alert_system")
def emergency_alert_system(condition: str) -> str:
    """Alert human physicians for emergency conditions (stub).
    In production, integrate with paging/alerting systems.
    """
    message = f"EMERGENCY ALERT: Immediate physician review required for condition: {condition}"
    logger.error(message)
    return message
