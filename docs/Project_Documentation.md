# Healthcare Diagnosis Support System (CrewAI)

This document provides a comprehensive overview of the system architecture, agents, tools, workflows, configuration, safety measures, and instructions to run and extend the project.

## 1. System Overview

- Multi-agent healthcare decision support built with CrewAI
- Sequential workflow: symptom analysis → history review → treatment → referral → safety check → follow-up → patient communication
- Pluggable tools for knowledge, EHR, scheduling, and clinical guidelines
- Safety measures enforced via validation and emergency alerts
- LLM provider: OpenAI (configurable via `.env`)

## 2. Project Structure

```
Health_Crew/
  README.md
  requirements.txt
  .env.example
  docs/
    Project_Documentation.md
  health_crew/
    __init__.py
    config.py
    llm.py
    safety.py
    agents.py
    tools.py
    tasks.py
    workflows.py
    app.py
    utils/
      __init__.py
      logging.py
```

## 3. Configuration

- Primary LLM
  - `OPENAI_API_KEY` (required)
  - `OPENAI_MODEL` default: `gpt-4o-mini`
- Optional external services
  - `GUIDELINES_API_URL` and `GUIDELINES_API_KEY` for clinical guidelines
  - `FHIR_BASE_URL` for EHR
  - `UMLS_API_KEY`, `RXNORM_API_KEY`, `DRUGBANK_API_KEY` for medical data
- Logging
  - `LOG_LEVEL` (default: INFO)

Edit `.env` accordingly (see `.env.example`).

## 4. LLM Integration (`health_crew/llm.py`)

- Uses CrewAI `LLM` wrapper with OpenAI
- Reads `OPENAI_API_KEY` and `OPENAI_MODEL`
- Configurable temperature and model

## 5. Agents (`health_crew/agents.py`)

- Symptom Analyzer
- Medical History Reviewer
- Treatment Recommendation Specialist
- Specialist Referral Coordinator
- Pharmaceutical Safety Analyst
- Care Coordination Scheduler
- Patient Communication Specialist

All agents share the same LLM instance via `llm.get_llm()` and use dedicated tools.

## 6. Tools (`health_crew/tools.py`)

- `medical_knowledge_search(query)` — stubbed knowledge search
- `drug_interaction_check(medications)` — stubbed interaction checker (with simple warning rule)
- `clinical_guidelines_search(condition)` — now resilient and can call an external API if configured, else returns a safe fallback summary
- `electronic_health_record_access(patient_id)` — stubbed FHIR access
- `appointment_scheduling(specialty, urgency)` — stubbed scheduler

## 7. Safety (`health_crew/safety.py`)

- `validate_medical_recommendation(recommendation)` — checks basic constraints; extend with real rules
- `emergency_alert_system(condition)` — logs alert; integrate with paging/notification system in production

## 8. Tasks (`health_crew/tasks.py`)

- Mirrors the 7 agents with clear expected outputs and inputs across steps

## 9. Workflow (`health_crew/workflows.py`)

- Builds a `Crew` with `Process.sequential` to enforce safe order of operations

## 10. CLI (`health_crew/app.py`)

- Interactive prompts for symptom input
- Runs the crew and prints the final output

## 11. Running the Project

1) Create venv and activate (Windows PowerShell)
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
2) Install dependencies
```
pip install -r requirements.txt
```
3) Configure environment
```
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4o-mini
```
4) Run
```
python -m health_crew.app
```

## 12. Extending the System

- Replace stubs with real integrations:
  - Clinical guidelines: set `GUIDELINES_API_URL` and `GUIDELINES_API_KEY`, API should expose `/guidelines?q=<condition>` returning `{ "summary": "...", "sources": [...] }`
  - Medical knowledge: integrate UMLS/SNOMED/ICD and add caching
  - Drug interactions: RxNorm/DrugBank/FDA
  - EHR: FHIR endpoints with auth
  - Scheduling: implement provider API calls
- Enhance safety validation:
  - Maintain a ruleset for contraindications and dosage ceilings
  - Add structured outputs with confidence scores and citations
- Observability:
  - Persist audit logs to a file or database
  - Use CrewAI tracing (CREWAI_TRACING_ENABLED=true) for in-depth runs

## 13. Compliance & Disclaimers

- Decision support only; requires physician review
- Handle PHI per HIPAA and local regulations
- Ensure appropriate disclaimers in patient-facing outputs

## 14. Troubleshooting

- If LLM calls fail, verify `OPENAI_API_KEY` and `OPENAI_MODEL`
- If guideline lookups fail, ensure `GUIDELINES_API_URL` and `GUIDELINES_API_KEY` are set and reachable
- Clear conflicting environment variables if unexpected models are used

## 15. Roadmap Ideas

- Add multi-condition reasoning with structured intermediate outputs
- Integrate lab/imaging data parsing
- Add persistent patient records and session resumes
- Build a small web UI for non-technical users
