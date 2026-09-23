from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MatchResponse(BaseModel):
    id: int
    candidate_id: int
    job_id: int
    match_score: float
    skill_score: Optional[float] = None
    experience_score: Optional[float] = None
    project_score: Optional[float] = None
    education_score: Optional[float] = None
    additional_skills_score: Optional[float] = None
    matching_skills: list[str] = []
    missing_skills: list[str] = []
    ai_explanation: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class RankingEntry(BaseModel):
    rank: int
    candidate_id: int
    candidate_name: Optional[str] = None
    file_name: str
    match_score: float
    matching_skills: list[str] = []
    missing_skills: list[str] = []