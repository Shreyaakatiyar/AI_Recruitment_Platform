from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CandidateResponse(BaseModel):
    id: int
    job_id: int
    file_name: str
    name: Optional[str] = None
    skills: list[str] = []
    experience_years: Optional[float] = None
    education: Optional[str] = None
    projects: list[str] = []
    certifications: list[str] = []
    created_at: datetime

    class Config:
        from_attributes = True