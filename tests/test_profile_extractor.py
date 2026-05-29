from app.services.profile_extractor import extract_candidate_name, extract_target_role


def test_extract_candidate_name():
    resume_text = """
    John Doe
    john.doe@email.com
    Python Developer
    """

    name = extract_candidate_name(resume_text)

    assert name == "John Doe"


def test_extract_target_role():
    job_description = "We are hiring a Machine Learning Engineer with Python experience."

    role = extract_target_role(job_description)

    assert role == "Machine Learning Engineer"


def test_extract_unknown_target_role():
    job_description = "We are hiring a technical profile with strong coding skills."

    role = extract_target_role(job_description)

    assert role == "Not specified"