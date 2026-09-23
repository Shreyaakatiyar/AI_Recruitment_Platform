from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class JobCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=255)
    raw_text: str = Field(..., min_length=20, description="Full job description text")


class JobResponse(BaseModel):
    id: int
    title: str
    raw_text: str
    required_skills: list[str] = []
    preferred_skills: list[str] = []
    min_experience_years: Optional[float] = None
    required_education: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True  