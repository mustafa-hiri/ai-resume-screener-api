from fastapi import FastAPI, UploadFile, File, Form
from schemas import ResumeAnalysisResponse
import uvicorn

app = FastAPI(
    title="AI Resume Screener API",
    description="Analyze a resume against a job description using AI.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {"message": "AI Resume Screener API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/analyze-resume", response_model= ResumeAnalysisResponse)
async def analyze_resume(
    resune_file: UploadFile = File(...),
    job_description: str = Form(...),
):
    return ResumeAnalysisResponse(
        candidate_name="Sample Candidate",
        target_role="AI Engineer",
        match_score=75,
        matched_skills=["Python", "FastAPI", "Machine Learning"],
        missing_skills=["Docker", "Kubernetes", "LLM Evaluation"],
        experience_fit="Good",
        education_fit="Strong",
        risk_flags=[
            "No clear production deployment experience",
            "Limited evidence of cloud infrastructure experience",
        ],
        recommended_improvements=[
            "Add deployed FastAPI project to resume",
            "Add Docker and cloud deployment experience",
            "Add measurable AI project evaluation results",
        ],
        interview_questions=[
            "How would you design an AI resume screening API?",
            "How would you validate the output of an LLM?",
            "How would you prevent hallucinated resume claims?",
        ],
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)