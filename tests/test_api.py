from io import BytesIO

from fastapi.testclient import TestClient
from reportlab.pdfgen import canvas

from app.main import app

client = TestClient(app)


def create_test_pdf(text: str) -> BytesIO:
    """
    Create a simple in-memory PDF file for API testing.
    """

    pdf_buffer = BytesIO()

    pdf = canvas.Canvas(pdf_buffer)
    pdf.drawString(100, 750, text)
    pdf.save()

    pdf_buffer.seek(0)

    return pdf_buffer


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


def test_analyze_resume_success():
    pdf_file = create_test_pdf(
        "John Doe has experience with Python, FastAPI, Docker, AWS, SQL, and testing."
    )

    response = client.post(
        "/analyze-resume",
        files={
            "resume_file": ("resume.pdf", pdf_file, "application/pdf")
        },
        data={
            "job_description": (
                "We are hiring a Machine Learning Engineer with Python, "
                "FastAPI, Docker, AWS, SQL, testing, and deployment experience."
            )
        },
    )

    response_data = response.json()

    assert response.status_code == 200
    assert "id" in response_data
    assert response_data["candidate_name"]
    assert response_data["target_role"] == "Machine Learning Engineer"
    assert response_data["match_score"] >= 0
    assert "Python" in response_data["matched_skills"]
    assert "Fastapi" in response_data["matched_skills"]
    assert "Docker" in response_data["matched_skills"]
    assert "Aws" in response_data["matched_skills"]
    assert "Sql" in response_data["matched_skills"]


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