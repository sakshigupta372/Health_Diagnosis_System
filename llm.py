from functools import lru_cache
from typing import Optional
from crewai import LLM
from .config import OPENAI_API_KEY, OPENAI_MODEL
from .utils.logging import get_logger

logger = get_logger(__name__)


@lru_cache(maxsize=1)
def get_llm(model: Optional[str] = None) -> LLM:
    """Return a shared OpenAI LLM (CrewAI wrapper) for all agents.

    Uses LiteLLM via provider-qualified model 'openai/<model>'.
    """
    if not OPENAI_API_KEY:
        logger.warning(
            "OPENAI_API_KEY is not set. OpenAI LLM will not function until it is provided."
        )
    base_model = model or OPENAI_MODEL
    logger.info("Initializing OpenAI LLM: %s", base_model)
    return LLM(
        model=base_model,
        api_key=OPENAI_API_KEY,
        temperature=0.2,
    )
