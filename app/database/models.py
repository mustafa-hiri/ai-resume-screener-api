from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database.db import Base


class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"

    id = Column(Integer, primary_key=True, index=True)
    candidate_name = Column(String, nullable=False)
    target_role = Column(String, nullable=False)
    match_score = Column(Integer, nullable=False)
    matched_skills = Column(Text, nullable=False)
    missing_skills = Column(Text, nullable=False)
    experience_fit = Column(String, nullable=False)
    education_fit = Column(String, nullable=False)
    risk_flags = Column(Text, nullable=False)
    recommended_improvements = Column(Text, nullable=False)
    interview_questions = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)