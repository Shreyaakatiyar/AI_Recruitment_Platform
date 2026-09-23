from typing import Optional
from pydantic import BaseModel, Field


class JobRequirementsExtraction(BaseModel):
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    min_experience_years: Optional[float] = None
    required_education: Optional[str] = None


class CandidateProfileExtraction(BaseModel):
    name: Optional[str] = None
    skills: list[str] = Field(default_factory=list)
    experience_years: Optional[float] = None
    education: Optional[str] = None
    projects: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)