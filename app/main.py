from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from app.schemas import ResumeAnalysisResponse
from app.services.resume_parser import extract_text_from_pdf
from app.services.jd_parser import extract_required_skills
from app.services.scoring import match_skills_with_resume, calculate_match_score
from app.services.profile_extractor import extract_candidate_name, extract_target_role
from app.services.report_generator import (
    determine_experience_fit,
    determine_education_fit,
    generate_risk_flags,
    generate_recommended_improvements,
    generate_interview_questions,
)


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


@app.post("/analyze-resume", response_model=ResumeAnalysisResponse)
async def analyze_resume(
    resume_file: UploadFile = File(...),
    job_description: str = Form(...),
):
    if not resume_file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    if not resume_file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        file_bytes = await resume_file.read()
        resume_text = extract_text_from_pdf(file_bytes)
        required_skills = extract_required_skills(job_description)
        matched_skills, missing_skills = match_skills_with_resume(required_skills=required_skills,resume_text=resume_text)
        match_score = calculate_match_score(matched_skills=matched_skills,required_skills=required_skills)
        candidate_name = extract_candidate_name(resume_text)
        target_role = extract_target_role(job_description)
        experience_fit = determine_experience_fit(match_score)
        education_fit = determine_education_fit(resume_text)
        risk_flags = generate_risk_flags(resume_text, missing_skills)
        recommended_improvements = generate_recommended_improvements(missing_skills)
        interview_questions = generate_interview_questions(
            target_role=target_role,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
) 



    except Exception as error:
        raise HTTPException(status_code=400, detail=f"PDF extraction failed: {str(error)}")

    if not resume_text:
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from the PDF. The PDF may be scanned or image-based.",
        )

    return ResumeAnalysisResponse(
        candidate_name= candidate_name,
        target_role=target_role,
        match_score=match_score,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        experience_fit=experience_fit,
        education_fit=education_fit,
        risk_flags=risk_flags,
        recommended_improvements=recommended_improvements,
        interview_questions=interview_questions,
        extracted_resume_preview=resume_text[:1000],
    )