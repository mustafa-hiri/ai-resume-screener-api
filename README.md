# AI Resume Screener API

An AI-powered backend API that compares a candidate resume against a job description and returns a structured hiring-fit analysis.

This project is built as a production-style AI Engineering portfolio project. It includes FastAPI, PDF parsing, rule-based scoring, SQLite storage, API tests, Docker support, and structured JSON responses.

## Problem

Recruiters and hiring teams often review many resumes manually. This takes time and can be inconsistent.

## Solution

This API accepts a resume PDF and a job description, extracts resume text, detects required job skills, compares them with the candidate profile, calculates a match score, identifies gaps, generates risk flags, and stores the analysis in a local SQLite database.

## Features

- Upload resume as PDF
- Submit job description text
- Extract resume text using PyMuPDF
- Extract required skills from job descriptions
- Match resume skills against job requirements
- Calculate match score from 0 to 100
- Detect candidate name
- Detect target role
- Generate experience fit and education fit
- Generate missing skills and risk flags
- Generate recommended improvements
- Generate interview questions
- Save analyses in SQLite
- Retrieve saved analyses
- Delete saved analyses
- Unit tests and API tests
- Docker support

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python |
| API Framework | FastAPI |
| Validation | Pydantic |
| PDF Parsing | PyMuPDF |
| Database | SQLite |
| ORM | SQLAlchemy |
| Testing | pytest |
| API Testing | FastAPI TestClient |
| Containerization | Docker |

## Project Architecture

```text
Resume PDF
    ↓
PDF Text Extraction
    ↓
Job Description Skill Parsing
    ↓
Resume Skill Matching
    ↓
Match Score Calculation
    ↓
Rule-Based Report Generation
    ↓
SQLite Storage
    ↓
Structured JSON API Response

## Run with Docker

Build the image:

```bash
docker build -t ai-resume-screener-api .
```
# Folder Structure
ai-resume-screener-api/
│
├── app/
│   ├── main.py
│   ├── schemas.py
│   ├── config.py
│   ├── services/
│   │   ├── resume_parser.py
│   │   ├── jd_parser.py
│   │   ├── scoring.py
│   │   ├── profile_extractor.py
│   │   └── report_generator.py
│   └── database/
│       ├── db.py
│       └── models.py
│
├── tests/
│   ├── test_api.py
│   ├── test_scoring.py
│   ├── test_jd_parser.py
│   └── test_profile_extractor.py
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── .env.example
├── .gitignore
└── README.md

# API Endpoints
| Method | Endpoint                  | Description                            |
| ------ | ------------------------- | -------------------------------------- |
| GET    | `/`                       | Root endpoint                          |
| GET    | `/health`                 | API health check                       |
| POST   | `/analyze-resume`         | Analyze resume against job description |
| GET    | `/analyses`               | Retrieve all saved analyses            |
| GET    | `/analysis/{analysis_id}` | Retrieve one saved analysis            |
| DELETE | `/analysis/{analysis_id}` | Delete one saved analysis              |

# Example Response
{
  "id": 1,
  "candidate_name": "John Doe",
  "target_role": "Machine Learning Engineer",
  "match_score": 71,
  "matched_skills": ["Python", "Fastapi", "Docker", "Aws", "Sql"],
  "missing_skills": ["Openai", "Langchain", "Rag"],
  "experience_fit": "Good",
  "education_fit": "Strong",
  "risk_flags": [
    "Some required skills are missing from the resume.",
    "No clear production deployment experience found."
  ],
  "recommended_improvements": [
    "Add evidence of Openai experience if you have it.",
    "Add evidence of Langchain experience if you have it.",
    "Add deployed project links, GitHub repositories, and technical metrics."
  ],
  "interview_questions": [
    "Why are you interested in this Machine Learning Engineer role?",
    "Describe one production-ready project you built from design to deployment.",
    "How have you used Python in a real project?"
  ],
  "extracted_resume_preview": "John Doe has experience with Python..."
}

# Current Limitations
Skill extraction is rule-based.
Resume parsing works best with text-based PDFs.
Scanned resumes are not supported yet.
No authentication yet.
No frontend yet.
OpenAI integration is planned but not yet added.


# Future Improvements
Add OpenAI structured output analysis
Add OCR for scanned resumes
Add PostgreSQL support
Add authentication
Add frontend dashboard
Add deployment to Render, Railway, or AWS
Add CI/CD with GitHub Actions
Add LLM evaluation metrics

# If yoy wanna clones this GitHub project follow these steps:

```cmd
git clone https://github.com/username/ai-resume-screener-api.git
cd ai-resume-screener-api
docker build -t ai-resume-screener-api .
docker run -p 8000:8000 ai-resume-screener-api
pip install --no-cache-dir -r requirements.txt
```
