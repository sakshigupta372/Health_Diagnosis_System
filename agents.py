from crewai import Agent
from .tools import (
    medical_knowledge_search,
    drug_interaction_check,
    clinical_guidelines_search,
    electronic_health_record_access,
    appointment_scheduling,
)
from .safety import validate_medical_recommendation, emergency_alert_system
from .llm import get_llm


# 1. Symptom Analyzer Agent
symptom_analyzer = Agent(
    role="Medical Symptom Analyst",
    goal="Analyze patient symptoms and identify potential conditions",
    backstory=(
        "Expert in symptom pattern recognition with deep knowledge of medical conditions, "
        "differential diagnosis, and symptom clustering."
    ),
    tools=[medical_knowledge_search, emergency_alert_system],
    allow_delegation=True,
    llm=get_llm(),
)

# 2. Medical History Reviewer Agent
history_reviewer = Agent(
    role="Medical History Analyst",
    goal="Comprehensively review patient medical history for relevant factors",
    backstory=(
        "Specialized in analyzing patient histories, identifying risk factors, contraindications, "
        "and relevant past conditions."
    ),
    tools=[electronic_health_record_access],
    allow_delegation=False,
    llm=get_llm(),
)

# 3. Treatment Recommendation Agent
treatment_agent = Agent(
    role="Treatment Recommendation Specialist",
    goal="Provide evidence-based treatment recommendations",
    backstory=(
        "Expert in clinical guidelines, treatment protocols, and evidence-based medicine "
        "with focus on personalized care."
    ),
    tools=[clinical_guidelines_search, validate_medical_recommendation],
    allow_delegation=True,
    llm=get_llm(),
)

# 4. Specialist Referral Agent
referral_agent = Agent(
    role="Specialist Referral Coordinator",
    goal="Determine appropriate specialist referrals and urgency",
    backstory=(
        "Expert in medical specialties, referral criteria, and healthcare system navigation."
    ),
    tools=[appointment_scheduling],
    allow_delegation=False,
    llm=get_llm(),
)

# 5. Drug Interaction Checker Agent
interaction_checker = Agent(
    role="Pharmaceutical Safety Analyst",
    goal="Ensure medication safety through comprehensive interaction analysis",
    backstory=(
        "Pharmacology expert specializing in drug interactions, contraindications, and adverse effect monitoring."
    ),
    tools=[drug_interaction_check, validate_medical_recommendation],
    allow_delegation=False,
    llm=get_llm(),
)

# 6. Follow-up Scheduler Agent
scheduler_agent = Agent(
    role="Care Coordination Scheduler",
    goal="Schedule appropriate follow-up care and monitoring",
    backstory=(
        "Healthcare coordinator expert in treatment timelines, monitoring schedules, and care continuity."
    ),
    tools=[appointment_scheduling],
    allow_delegation=False,
    llm=get_llm(),
)

# 7. Patient Communication Agent
communication_agent = Agent(
    role="Patient Communication Specialist",
    goal="Translate medical information into clear, actionable patient guidance",
    backstory=(
        "Expert in medical communication, patient education, and health literacy with focus on clear, empathetic communication."
    ),
    tools=[],
    allow_delegation=False,
    llm=get_llm(),
)
