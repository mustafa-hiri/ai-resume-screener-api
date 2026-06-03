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


def test_get_all_analyses():
    response = client.get("/analyses")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_analysis_not_found():
    response = client.get("/analysis/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Analysis not found."


def test_delete_analysis_not_found():
    response = client.delete("/analysis/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Analysis not found."