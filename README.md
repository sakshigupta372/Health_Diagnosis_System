# Healthcare Diagnosis Support System (CrewAI)

This project implements a multi-agent Healthcare Diagnosis Support System using CrewAI with advanced medical imaging analysis. It includes:

- **Symptom analysis** - AI-powered symptom pattern recognition
- **Medical history review** - Comprehensive patient history analysis
- **Medical imaging analysis** - X-ray, MRI, CT scan interpretation using Gemini Vision
- **Treatment recommendations** - Evidence-based treatment planning
- **Drug interaction checking** - Pharmaceutical safety validation
- **Specialist referrals** - Automated referral coordination
- **Follow-up scheduling** - Care continuity management
- **Patient-facing communication** - Clear, empathetic guidance

Critical safety, validation, and audit logging are included to ensure physician oversight and compliance considerations.

## Web UI

The system includes a modern Streamlit web interface (`streamlit_app.py`) with:
- Patient information form
- Medical image upload and analysis
- Real-time multi-agent processing
- Comprehensive diagnosis reports
- API key validation and configuration

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

1. **Create and activate a virtual environment** (recommended)

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

2. **Install dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Configure environment variables**

   Copy `.env.example` to `.env` and fill in values:

   **Required:**
   - `OPENAI_API_KEY` - Your OpenAI API key (for LLM agents)
   - `GOOGLE_API_KEY` - Your Google AI API key (for medical imaging analysis)

   **Optional:**
   - `OPENAI_MODEL` (defaults to `gpt-4o-mini`)
   - `GEMINI_MODEL` (defaults to `gemini-1.5-pro-latest`)
   - `LOG_LEVEL` (defaults to `INFO`)

   Optional integrations for EHR/Guidelines/Pharmacy can be added later.

4. **Run the Web UI** (Recommended)

   ```bash
   streamlit run streamlit_app.py
   ```

   Open your browser to the displayed URL (typically http://localhost:8501). You can:
   - Enter patient symptoms, demographics, history
   - Upload medical images (X-ray, MRI, CT scans)
   - Run multi-agent diagnosis with or without imaging
   - View comprehensive diagnosis reports

5. **Or run the CLI demo**

   ```bash
   python -m health_crew.app
   ```

   You will be prompted to enter a mock patient case. The crew will run sequentially and print results.

## Medical Imaging Analysis

The system includes advanced medical imaging analysis powered by Google's Gemini Vision model:

### Supported Image Types
- X-rays (chest, bone, dental)
- MRI scans
- CT scans  
- Ultrasound images
- Other medical imaging modalities

### Capabilities
- **Automatic modality detection** - Identifies imaging type and anatomical region
- **Finding extraction** - Detects and describes abnormalities
- **Severity assessment** - Rates findings as Normal/Mild/Moderate/Severe
- **Diagnostic interpretation** - Provides differential diagnoses with confidence levels
- **Patient-friendly explanations** - Translates technical findings into clear language
- **Timeline comparison** - Compares current and previous images to track progression

### Usage
In the Streamlit UI, simply upload a medical image alongside patient information. The imaging analyst agent will automatically:
1. Analyze the image using Gemini Vision
2. Extract key findings and measurements
3. Integrate findings with patient symptoms and history
4. Include imaging results in the comprehensive diagnosis report

## Environment Variables

See `.env.example` for available variables.

### Required
- `OPENAI_API_KEY` - Your OpenAI API key (for LLM agents)
- `GOOGLE_API_KEY` - Your Google AI API key (for medical imaging with Gemini Vision)

### Optional LLM Configuration
- `OPENAI_MODEL` - e.g., `gpt-4o-mini` (default)
- `GEMINI_MODEL` - e.g., `gemini-1.5-pro-latest` (default for imaging)
- `LOG_LEVEL` - Logging verbosity: DEBUG, INFO, WARNING, ERROR

### Optional External Integrations (stubs provided)
- `UMLS_API_KEY`, `RXNORM_API_KEY`, `DRUGBANK_API_KEY` - Medical terminology and drug databases
- `FHIR_BASE_URL` - FHIR-compliant EHR integration
- `SCHEDULER_BASE_URL` - Appointment scheduling system
- `GUIDELINES_API_URL`, `GUIDELINES_API_KEY` - Clinical guidelines repository
  - To enable live clinical guidelines: The endpoint should support `GET /guidelines?q=<condition>` and return `{ "summary": "..." }`

### Tracing
- `CREWAI_TRACING_ENABLED=true` - Enable CrewAI execution traces for debugging

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
