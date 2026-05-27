from fastapi import FastAPI

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