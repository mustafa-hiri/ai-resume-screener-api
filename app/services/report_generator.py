from typing import List


def determine_experience_fit(match_score: int) -> str:
    """
    Determine experience fit based on the match score.
    """

    if match_score >= 80:
        return "Strong"

    if match_score >= 60:
        return "Good"

    if match_score >= 40:
        return "Moderate"

    return "Weak"


def determine_education_fit(resume_text: str) -> str:
    """
    Determine education fit using simple keyword matching.
    """

    resume_text_lower = resume_text.lower()

    education_keywords = [
        "phd",
        "doctorate",
        "master",
        "bachelor",
        "degree",
        "university",
        "engineering",
        "computer science",
        "machine learning",
        "data science",
    ]

    for keyword in education_keywords:
        if keyword in resume_text_lower:
            return "Strong"

    return "Not clearly specified"


def generate_risk_flags(
    resume_text: str,
    missing_skills: List[str],
) -> List[str]:
    """
    Generate risk flags based on missing skills and resume content.
    """

    resume_text_lower = resume_text.lower()
    risk_flags = []

    if missing_skills:
        risk_flags.append("Some required skills are missing from the resume.")

    if "docker" not in resume_text_lower:
        risk_flags.append("No clear Docker experience found.")

    if "deploy" not in resume_text_lower and "deployment" not in resume_text_lower:
        risk_flags.append("No clear production deployment experience found.")

    if "aws" not in resume_text_lower and "azure" not in resume_text_lower and "gcp" not in resume_text_lower:
        risk_flags.append("No clear cloud platform experience found.")

    if "test" not in resume_text_lower and "pytest" not in resume_text_lower:
        risk_flags.append("No clear testing experience found.")

    if not risk_flags:
        risk_flags.append("No major risk flags detected.")

    return risk_flags


def generate_recommended_improvements(missing_skills: List[str]) -> List[str]:
    """
    Generate resume improvement recommendations.
    """

    improvements = []

    for skill in missing_skills[:5]:
        improvements.append(f"Add evidence of {skill} experience if you have it.")

    if not improvements:
        improvements.append("Add more measurable achievements and project impact.")

    improvements.append("Add deployed project links, GitHub repositories, and technical metrics.")

    return improvements


def generate_interview_questions(
    target_role: str,
    matched_skills: List[str],
    missing_skills: List[str],
) -> List[str]:
    """
    Generate basic interview questions from matched and missing skills.
    """

    questions = [
        f"Why are you interested in this {target_role} role?",
        "Describe one production-ready project you built from design to deployment.",
    ]

    for skill in matched_skills[:3]:
        questions.append(f"How have you used {skill} in a real project?")

    for skill in missing_skills[:3]:
        questions.append(f"How would you learn or apply {skill} for this role?")

    questions.append("How would you evaluate the reliability of an AI-based resume screening system?")

    return questions