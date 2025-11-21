# Healthcare Diagnosis Support System (CrewAI)

This project implements a multi-agent Healthcare Diagnosis Support System using CrewAI. It includes:

- Symptom analysis
- Medical history review
- Treatment recommendations
- Specialist referrals
- Follow-up scheduling
- Patient-facing communication

Critical safety, validation, and audit logging are included to ensure physician oversight and compliance considerations.

## Features

- Crew of domain-specialized agents with dedicated tools and tasks
- Sequential workflow ensuring safety checkpoints and validations
- Pluggable tool layer for real API integrations (UMLS, RxNorm, EHR/FHIR, DrugBank, etc.)
- Config-driven setup via environment variables
- Simple CLI entry point (`python -m health_crew.app`) for demonstration
- OpenAI LLM support via CrewAI's native LLM wrapper (primary)

## Project Structure

Health_Crew/
{{ ... }}
    safety.py
    agents.py
    tools.py
    tasks.py
    workflows.py
    app.py
    utils/
      __init__.py
      logging.py

## Quickstart

1. Create and activate a virtual environment (recommended)

{{ ... }}
   pip install -r requirements.txt
   ```

3. Configure environment variables

   Copy `.env.example` to `.env` and fill in values. For OpenAI:

   - `OPENAI_API_KEY` (required)
   - `OPENAI_MODEL` (optional, defaults to `gpt-4o-mini`)

   Optional integrations for EHR/Guidelines/Pharmacy can be added later.

4. Run the demo CLI

   ```bash
   python -m health_crew.app
   ```

   You will be prompted to enter a mock patient case. The crew will run sequentially (OpenAI model will be shown) and print a summarized result.

## Environment Variables

See `.env.example` for available variables. Key ones for LLM:

- `OPENAI_API_KEY`: Your OpenAI API key.
- `OPENAI_MODEL`: e.g., `gpt-4o-mini` (default).

Optional (stubs provided):
- `UMLS_API_KEY`, `RXNORM_API_KEY`, `DRUGBANK_API_KEY`, `FHIR_BASE_URL`, `SCHEDULER_BASE_URL`, `GUIDELINES_API_URL`.
  - To enable live clinical guidelines: set `GUIDELINES_API_URL` and `GUIDELINES_API_KEY`. The endpoint is expected to support `GET /guidelines?q=<condition>` and return `{ "summary": "..." }`.

Tracing (optional):
- `CREWAI_TRACING_ENABLED=true` to enable CrewAI execution traces.

## Notes on Safety and Compliance

- This system is designed strictly for decision support. All outputs require human physician review and approval.
- Emergency flags trigger an `emergency_alert_system` tool call for immediate escalation.
- The `validate_medical_recommendation` tool enforces dosage limits, interactions, and guideline checks (extend with real rulesets).
- Logging with provenance and confidence scoring is enabled in `utils/logging.py`.

## Extending Integrations

Implement the placeholders in `tools.py` to integrate with:

- UMLS, SNOMED CT, ICD-10/11
- RxNorm, DrugBank, FDA datasets
- FHIR-compliant EHRs
- Scheduling systems
- Clinical guideline repositories
Update `config.py` to load necessary API keys and endpoints, and ensure rate-limiting and error handling as needed.
