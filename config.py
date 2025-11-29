import os
from pathlib import Path
from dotenv import load_dotenv

# Load env from project root, then package dir, then CWD defaults
_ROOT_ENV = Path(__file__).resolve().parents[1] / ".env"
_PKG_ENV = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=_ROOT_ENV, override=False)
load_dotenv(dotenv_path=_PKG_ENV, override=False)
load_dotenv(override=False)

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
APP_ENV = os.getenv("APP_ENV", "development")

# External APIs (optional)
UMLS_API_KEY = os.getenv("UMLS_API_KEY")
RXNORM_API_KEY = os.getenv("RXNORM_API_KEY")
DRUGBANK_API_KEY = os.getenv("DRUGBANK_API_KEY")
FHIR_BASE_URL = os.getenv("FHIR_BASE_URL")
SCHEDULER_BASE_URL = os.getenv("SCHEDULER_BASE_URL")
GUIDELINES_API_URL = os.getenv("GUIDELINES_API_URL")
GUIDELINES_API_KEY = os.getenv("GUIDELINES_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-pro-latest")

# OpenAI (primary LLM provider)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
