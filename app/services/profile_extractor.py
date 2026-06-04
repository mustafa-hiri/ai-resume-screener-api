import re


def extract_candidate_name(resume_text: str) -> str:
    """
    Extract a candidate name from the first lines of a resume.

    This is a simple rule-based extractor.
    It assumes the candidate name is usually near the top of the resume.
    """

    lines = resume_text.splitlines()

    cleaned_lines = [
        line.strip()
        for line in lines
        if line.strip()
    ]

    if not cleaned_lines:
        return "Unknown Candidate"

    for line in cleaned_lines[:10]:
        lower_line = line.lower()

        if "email" in lower_line:
            continue

        if "phone" in lower_line:
            continue

        if "linkedin" in lower_line:
            continue

        if "github" in lower_line:
            continue

        if "resume" in lower_line:
            continue

        if re.search(r"\d", line):
            continue

        words = line.split()

        if 2 <= len(words) <= 4:
            return line

    return cleaned_lines[0]


def extract_target_role(job_description: str) -> str:
    """
    Extract a probable target role from the job description.
    """

    patterns = [
        r"role:\s*([A-Za-z0-9\s\/\-\+]+)",
        r"job title:\s*([A-Za-z0-9\s\/\-\+]+)",
        r"position:\s*([A-Za-z0-9\s\/\-\+]+)",
        r"title:\s*([A-Za-z0-9\s\/\-\+]+)",
        r"we are hiring (?:a|an)?\s*([A-Za-z0-9\s\/\-\+]+)",
        r"join our .* as (?:a|an)?\s*([A-Za-z0-9\s\/\-\+]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, job_description, re.IGNORECASE)

        if match:
            role = match.group(1).strip()

            role = re.split(
                r"\n|\.|,| at | with | in ",
                role,
                flags=re.IGNORECASE,
            )[0].strip()

            if 2 <= len(role.split()) <= 6:
                return role

    known_roles = [
        "AI Engineer",
        "Machine Learning Engineer",
        "Deep Learning Engineer",
        "Deep Learning Intern",
        "Machine Learning Intern",
        "AI Intern",
        "Perception Intern",
        "Computer Vision Intern",
        "Computer Vision Engineer",
        "Data Scientist",
        "Data Analyst",
        "Backend Engineer",
        "Software Engineer",
        "NLP Engineer",
        "MLOps Engineer",
        "LLM Engineer",
        "Research Scientist",
        "Robotics Engineer",
    ]

    job_description_lower = job_description.lower()

    for role in known_roles:
        if role.lower() in job_description_lower:
            return role

    return "Not specified"