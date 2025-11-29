from crewai import Crew, Process
from .agents import (
    symptom_analyzer,
    history_reviewer,
    treatment_agent,
    referral_agent,
    interaction_checker,
    scheduler_agent,
    communication_agent,
)
from .tasks import (
    symptom_analysis_task,
    history_review_task,
    treatment_recommendation_task,
    referral_assessment_task,
    drug_safety_check_task,
    follow_up_scheduling_task,
    patient_communication_task,
)


def build_diagnosis_crew(verbose: bool = True) -> Crew:
    agents = [
        symptom_analyzer,
        history_reviewer,
        treatment_agent,
        referral_agent,
        interaction_checker,
        scheduler_agent,
        communication_agent,
    ]
    tasks = [
        symptom_analysis_task,
        history_review_task,
        treatment_recommendation_task,
        referral_assessment_task,
        drug_safety_check_task,
        follow_up_scheduling_task,
        patient_communication_task,
    ]
    crew = Crew(agents=agents, tasks=tasks, process=Process.sequential, verbose=verbose)
    return crew
