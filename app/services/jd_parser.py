from typing import List


COMMON_SKILLS = [
    "python",
    "fastapi",
    "flask",
    "django",
    "machine learning",
    "deep learning",
    "pytorch",
    "tensorflow",
    "scikit-learn",
    "pandas",
    "numpy",
    "sql",
    "postgresql",
    "sqlite",
    "mongodb",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "openai",
    "langchain",
    "llm",
    "rag",
    "vector database",
    "faiss",
    "chroma",
    "qdrant",
    "api",
    "rest api",
    "git",
    "github",
    "ci/cd",
    "linux",
]


def extract_required_skills(job_description: str) -> List[str]:
    """
    Extract required skills from a job description using keyword matching.

    Args:
        job_description: Job description text submitted by the user.

    Returns:
        A list of detected required skills.
    """

    job_description_lower = job_description.lower()

    detected_skills = []

    for skill in COMMON_SKILLS:
        if skill in job_description_lower:
            detected_skills.append(skill.title())

    return detected_skills