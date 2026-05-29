from app.services.scoring import match_skills_with_resume, calculate_match_score


def test_match_skills_with_resume():
    required_skills = ["Python", "FastAPI", "Docker"]
    resume_text = "I have experience with Python and FastAPI."

    matched_skills, missing_skills = match_skills_with_resume(
        required_skills=required_skills,
        resume_text=resume_text,
    )

    assert matched_skills == ["Python", "FastAPI"]
    assert missing_skills == ["Docker"]


def test_calculate_match_score():
    matched_skills = ["Python", "FastAPI"]
    required_skills = ["Python", "FastAPI", "Docker", "AWS"]

    score = calculate_match_score(
        matched_skills=matched_skills,
        required_skills=required_skills,
    )

    assert score == 50


def test_calculate_match_score_with_no_required_skills():
    matched_skills = []
    required_skills = []

    score = calculate_match_score(
        matched_skills=matched_skills,
        required_skills=required_skills,
    )

    assert score == 0