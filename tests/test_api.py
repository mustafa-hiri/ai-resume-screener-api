from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "AI Resume Screener API"}


def test_analyze_resume_rejects_non_pdf():
    fake_file_content = b"This is not a PDF file."

    response = client.post(
        "/analyze-resume",
        files={
            "resume_file": ("resume.txt", fake_file_content, "text/plain")
        },
        data={
            "job_description": "We need a Python FastAPI developer."
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Only PDF files are supported."