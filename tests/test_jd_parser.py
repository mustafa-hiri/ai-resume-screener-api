from app.services.jd_parser import extract_required_skills


def test_extract_required_skills():
    job_description = """
    We are hiring a Machine Learning Engineer with Python, FastAPI,
    Docker, AWS, SQL, and OpenAI experience.
    """

    skills = extract_required_skills(job_description)

    assert "Python" in skills
    assert "Fastapi" in skills
    assert "Docker" in skills
    assert "Aws" in skills
    assert "Sql" in skills
    assert "Openai" in skills