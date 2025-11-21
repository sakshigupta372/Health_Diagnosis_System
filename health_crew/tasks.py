from crewai import Task
from .agents import (
    symptom_analyzer,
    history_reviewer,
    treatment_agent,
    referral_agent,
    interaction_checker,
    scheduler_agent,
    communication_agent,
)

# Task: Symptom analysis
symptom_analysis_task = Task(
    description=(
        "Analyze the patient's presented symptoms:\n"
        "- Categorize and prioritize symptoms\n"
        "- Assess severity and urgency\n"
        "- Identify potential conditions\n"
        "- Flag any emergency conditions\n\n"
        "Patient Symptoms: {symptoms}\n"
        "Demographics: {demographics}\n"
    ),
    agent=symptom_analyzer,
    expected_output="Structured symptom analysis with differential diagnosis list",
)

# Task: Medical history review
history_review_task = Task(
    description=(
        "Review patient medical history:\n"
        "- Analyze past conditions and treatments\n"
        "- Identify risk factors and contraindications\n"
        "- Review medication history and allergies\n"
        "- Assess family history relevance\n\n"
        "History: {history}\n"
        "Current Medications: {medications}\n"
    ),
    agent=history_reviewer,
    expected_output="Comprehensive medical history summary with risk assessment",
)

# Task: Treatment recommendations
treatment_recommendation_task = Task(
    description=(
        "Generate evidence-based treatment recommendations:\n"
        "- Develop treatment plan options\n"
        "- Consider patient-specific factors\n"
        "- Include medication recommendations\n"
        "- Specify monitoring requirements\n\n"
        "Working Differential: {working_differential}\n"
    ),
    agent=treatment_agent,
    expected_output="Detailed treatment plan with alternatives and monitoring",
)

# Task: Referral assessment
referral_assessment_task = Task(
    description=(
        "Assess need for specialist consultation and referral urgency based on:\n"
        "- Conditions and risk\n"
        "- Availability\n"
        "- Appropriate specialty\n\n"
        "Diagnosis Summary: {diagnosis_summary}\n"
    ),
    agent=referral_agent,
    expected_output="Referral plan with specialty, urgency, and any scheduling steps",
)

# Task: Drug safety check
drug_safety_check_task = Task(
    description=(
        "Perform drug interaction and contraindication checks for the proposed plan.\n"
        "Proposed Medications: {proposed_medications}\n"
        "Allergies: {allergies}\n"
        "Conditions: {conditions}\n"
    ),
    agent=interaction_checker,
    expected_output="List of interaction warnings, contraindications, and dosing considerations",
)

# Task: Follow-up scheduling
follow_up_scheduling_task = Task(
    description=(
        "Schedule appropriate follow-up care and monitoring.\n"
        "Treatment Plan: {treatment_plan}\n"
        "Referral Plan: {referral_plan}\n"
    ),
    agent=scheduler_agent,
    expected_output="Follow-up schedule, reminders, and monitoring checkpoints",
)

# Task: Patient communication
patient_communication_task = Task(
    description=(
        "Translate the clinical plan into clear patient guidance including:\n"
        "- What to do now\n"
        "- What to watch for (red flags)\n"
        "- When to seek help\n"
        "- Follow-up expectations\n\n"
        "Clinical Summary: {clinical_summary}\n"
    ),
    agent=communication_agent,
    expected_output="Clear, empathetic patient-facing instructions and summary",
)
