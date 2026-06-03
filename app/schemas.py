from pydantic import BaseModel, Field
from typing import List


class ResumeAnalysisResponse(BaseModel):
    candidate_name: str = Field(description="Detected candidate name")
    target_role: str = Field(description="Target job role")
    match_score: int = Field(ge=0, le=100, description="Match score from 0 to 100")
    matched_skills: List[str]
    missing_skills: List[str]
    experience_fit: str
    education_fit: str
    risk_flags: List[str]
    recommended_improvements: List[str]
    interview_questions: List[str]
    extracted_resume_preview: str


class SavedAnalysisResponse(ResumeAnalysisResponse):
    id: int