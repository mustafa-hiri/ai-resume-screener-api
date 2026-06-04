import json
from typing import List

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session

from app.schemas import SavedAnalysisResponse
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
from app.services.ai_analyzer import analyze_resume_with_ai
from app.database.db import Base, engine, get_db
from app.database.models import ResumeAnalysis


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Resume Screener API",
    description="Analyze a resume against a job description using AI.",
    version="0.1.0",
)


def convert_analysis_to_response(analysis: ResumeAnalysis) -> SavedAnalysisResponse:
    return SavedAnalysisResponse(
        id=analysis.id,
        candidate_name=analysis.candidate_name,
        target_role=analysis.target_role,
        match_score=analysis.match_score,
        matched_skills=json.loads(analysis.matched_skills),
        missing_skills=json.loads(analysis.missing_skills),
        experience_fit=analysis.experience_fit,
        education_fit=analysis.education_fit,
        risk_flags=json.loads(analysis.risk_flags),
        recommended_improvements=json.loads(analysis.recommended_improvements),
        interview_questions=json.loads(analysis.interview_questions),
        extracted_resume_preview="Saved analysis preview not stored.",
    )


@app.get("/")
def root():
    return {"message": "AI Resume Screener API"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/analyze-resume", response_model=SavedAnalysisResponse)
async def analyze_resume(
    resume_file: UploadFile = File(...),
    job_description: str = Form(...),
    db: Session = Depends(get_db),
):
    if not resume_file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    if not resume_file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        file_bytes = await resume_file.read()
        resume_text = extract_text_from_pdf(file_bytes)

        if not resume_text:
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from the PDF. The PDF may be scanned or image-based.",
            )

        required_skills = extract_required_skills(job_description)

        matched_skills, missing_skills = match_skills_with_resume(
            required_skills=required_skills,
            resume_text=resume_text,
        )

        match_score = calculate_match_score(
            matched_skills=matched_skills,
            required_skills=required_skills,
        )

        try:
            ai_result = analyze_resume_with_ai(
                resume_text=resume_text,
                job_description=job_description,
            )

            candidate_name = ai_result.candidate_name
            target_role = ai_result.target_role
            match_score = ai_result.match_score
            matched_skills = ai_result.matched_skills
            missing_skills = ai_result.missing_skills
            experience_fit = ai_result.experience_fit
            education_fit = ai_result.education_fit
            risk_flags = ai_result.risk_flags
            recommended_improvements = ai_result.recommended_improvements
            interview_questions = ai_result.interview_questions

        except Exception as ai_error:
            print(f"OpenAI analysis failed: {ai_error}")

            candidate_name = extract_candidate_name(resume_text)
            target_role = extract_target_role(job_description)
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

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(status_code=400, detail=f"Processing failed: {str(error)}")

    saved_analysis = ResumeAnalysis(
        candidate_name=candidate_name,
        target_role=target_role,
        match_score=match_score,
        matched_skills=json.dumps(matched_skills),
        missing_skills=json.dumps(missing_skills),
        experience_fit=experience_fit,
        education_fit=education_fit,
        risk_flags=json.dumps(risk_flags),
        recommended_improvements=json.dumps(recommended_improvements),
        interview_questions=json.dumps(interview_questions),
    )

    db.add(saved_analysis)
    db.commit()
    db.refresh(saved_analysis)

    return SavedAnalysisResponse(
        id=saved_analysis.id,
        candidate_name=candidate_name,
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


@app.get("/analyses", response_model=List[SavedAnalysisResponse])
def get_all_analyses(db: Session = Depends(get_db)):
    analyses = db.query(ResumeAnalysis).order_by(ResumeAnalysis.id.desc()).all()

    return [
        convert_analysis_to_response(analysis)
        for analysis in analyses
    ]


@app.get("/analysis/{analysis_id}", response_model=SavedAnalysisResponse)
def get_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
):
    analysis = db.query(ResumeAnalysis).filter(ResumeAnalysis.id == analysis_id).first()

    if analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found.")

    return convert_analysis_to_response(analysis)


@app.delete("/analysis/{analysis_id}")
def delete_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
):
    analysis = db.query(ResumeAnalysis).filter(ResumeAnalysis.id == analysis_id).first()

    if analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found.")

    db.delete(analysis)
    db.commit()

    return {"message": "Analysis deleted successfully."}