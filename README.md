# AI Resume Screener API

An AI-powered backend API that compares a candidate resume against a job description and returns a structured hiring-fit analysis.

This project is built as a production-style AI Engineering portfolio project. It includes FastAPI, PDF parsing, OpenAI structured analysis, rule-based fallback scoring, SQLite storage, API tests, Docker support, and structured JSON responses.

## Problem

Recruiters and hiring teams often review many resumes manually. This process can be slow, inconsistent, and difficult to standardize across many candidates.

## Solution

This API accepts a resume PDF and a job description, extracts resume text, analyzes the candidate profile against the job requirements, calculates a match score, identifies missing skills, generates risk flags, recommends improvements, creates interview questions, and stores the analysis in a local SQLite database.

The project supports two analysis modes:

- **AI mode**: uses OpenAI Structured Outputs to generate a structured hiring-fit analysis.
- **Fallback mode**: uses deterministic rule-based parsing and scoring if OpenAI is unavailable or disabled.

## Features

- Upload resume as PDF
- Submit job description text
- Extract resume text using PyMuPDF
- Analyze resume with OpenAI Structured Outputs
- Rule-based fallback when OpenAI is unavailable
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
| AI Integration | OpenAI API |
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
Job Description Parsing
    ↓
Rule-Based Baseline Scoring
    ↓
OpenAI Structured Analysis
    ↓
Fallback Logic if OpenAI Fails
    ↓
SQLite Storage
    ↓
Structured JSON API Response
```

## Folder Structure

```text
ai-resume-screener-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   ├── config.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── resume_parser.py
│   │   ├── jd_parser.py
│   │   ├── scoring.py
│   │   ├── profile_extractor.py
│   │   ├── report_generator.py
│   │   └── ai_analyzer.py
│   └── database/
│       ├── __init__.py
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
├── .dockerignore
└── README.md
```

## Main Files

| File | Purpose |
|---|---|
| `app/main.py` | Main FastAPI application and API endpoints |
| `app/schemas.py` | Pydantic models for structured API responses |
| `app/config.py` | Loads environment variables such as OpenAI API key and model |
| `app/services/resume_parser.py` | Extracts text from uploaded PDF resumes |
| `app/services/jd_parser.py` | Extracts required skills from job descriptions |
| `app/services/scoring.py` | Matches resume skills with job requirements and calculates score |
| `app/services/profile_extractor.py` | Extracts candidate name and target role using fallback rules |
| `app/services/report_generator.py` | Generates fallback analysis report fields |
| `app/services/ai_analyzer.py` | Uses OpenAI API for structured resume analysis |
| `app/database/db.py` | Configures SQLite database connection |
| `app/database/models.py` | Defines SQLAlchemy database model |
| `tests/` | Contains automated unit and API tests |
| `Dockerfile` | Defines the Docker image build process |
| `docker-compose.yml` | Runs the app using Docker Compose |
| `.env.example` | Shows required environment variables without exposing secrets |
| `.gitignore` | Prevents private or unnecessary files from being pushed to GitHub |
| `.dockerignore` | Prevents unnecessary files from being copied into the Docker image |

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Root endpoint |
| GET | `/health` | API health check |
| POST | `/analyze-resume` | Analyze resume against job description |
| GET | `/analyses` | Retrieve all saved analyses |
| GET | `/analysis/{analysis_id}` | Retrieve one saved analysis |
| DELETE | `/analysis/{analysis_id}` | Delete one saved analysis |

## Example Response

```json
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
```

## Environment Variables

Create a `.env` file in the project root.

```text
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4.1-nano
```

Use `.env.example` as a template.

Do not commit your real `.env` file to GitHub.

## Run Locally

Clone the repository:

```bash
git clone https://github.com/username/ai-resume-screener-api.git
cd ai-resume-screener-api
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```cmd
.venv\Scripts\activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the API:

```bash
python -m uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Run Without OpenAI

To force rule-based fallback mode during testing or development:

```cmd
set DISABLE_OPENAI=true
python -m uvicorn app.main:app --reload
```

To enable OpenAI again:

```cmd
set DISABLE_OPENAI=
python -m uvicorn app.main:app --reload
```

## Run Tests

Run all tests:

```bash
python -m pytest
```

To avoid calling OpenAI during tests:

```cmd
set DISABLE_OPENAI=true
python -m pytest
```

## Run with Docker

Build the Docker image:

```bash
docker build -t ai-resume-screener-api .
```

Run the container:

```bash
docker run -p 8000:8000 ai-resume-screener-api
```

Open:

```text
http://127.0.0.1:8000/docs
```

Using Docker Compose:

```bash
docker compose up --build
```

## Database

The project uses SQLite.

After running an analysis, this local database file is created:

```text
resume_screener.db
```

The database stores saved analyses in the `resume_analyses` table.

The database file is ignored by Git because it may contain private resume data.

## Security Notes

Do not commit these files or folders to GitHub:

```text
.env
resume_screener.db
uploads/
.venv/
venv/
__pycache__/
```

The `.gitignore` file should include:

```gitignore
.env
*.db
.venv/
venv/
__pycache__/
uploads/
```

The `.dockerignore` file should include:

```gitignore
__pycache__/
*.pyc
.env
.venv/
venv/
.git/
.pytest_cache/
*.db
uploads/
screenshots/
```

## Current Limitations

- Resume parsing works best with text-based PDFs.
- Scanned resumes are not supported yet.
- Skill extraction fallback is rule-based.
- No authentication yet.
- No frontend dashboard yet.
- SQLite is used for local development only.
- OpenAI API usage requires a valid API key and API billing setup.

## Future Improvements

- Add OCR for scanned resumes
- Add PostgreSQL support
- Add authentication
- Add frontend dashboard
- Add deployment to Render, Railway, or AWS
- Add CI/CD with GitHub Actions
- Add LLM evaluation metrics
- Add duplicate analysis detection to reduce API cost
- Add candidate ranking across multiple resumes

## Screenshots

Add screenshots after testing the API locally:

```text
screenshots/swagger-docs.png
screenshots/health-endpoint.png
screenshots/analyze-resume-response.png
screenshots/saved-analyses.png
```

Example Markdown:

```markdown
![Swagger Docs](screenshots/swagger-docs.png)
![Analyze Resume Response](screenshots/analyze-resume-response.png)
```

## Project Status

In development.

Completed components:

- FastAPI backend
- PDF resume upload
- PDF text extraction
- Rule-based skill matching
- OpenAI structured analysis
- Rule-based fallback mode
- SQLite database storage
- Saved analysis retrieval
- Saved analysis deletion
- Unit tests
- API tests
- Docker support