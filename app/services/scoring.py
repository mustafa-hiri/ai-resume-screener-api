from typing import List, Tuple


def match_skills_with_resume(
    required_skills: List[str],
    resume_text: str,
) -> Tuple[List[str], List[str]]:
    """
    Compare required job skills with resume text.

    Args:
        required_skills: Skills extracted from the job description.
        resume_text: Text extracted from the resume PDF.

    Returns:
        A tuple containing:
        - matched skills
        - missing skills
    """

    resume_text_lower = resume_text.lower()

    matched_skills = []
    missing_skills = []

    for skill in required_skills:
        skill_lower = skill.lower()

        if skill_lower in resume_text_lower:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    return matched_skills, missing_skills


def calculate_match_score(
    matched_skills: List[str],
    required_skills: List[str],
) -> int:
    """
    Calculate match score based on matched required skills.

    Args:
        matched_skills: Skills found in the resume.
        required_skills: Skills required by the job description.

    Returns:
        Match score from 0 to 100.
    """

    if not required_skills:
        return 0

    score = (len(matched_skills) / len(required_skills)) * 100

    return round(score)