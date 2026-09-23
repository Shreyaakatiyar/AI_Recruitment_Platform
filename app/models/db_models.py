from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    raw_text = Column(Text, nullable=False)

    required_skills = Column(JSON, default=list)
    preferred_skills = Column(JSON, default=list)
    min_experience_years = Column(Float, nullable=True)
    required_education = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    candidates = relationship("Candidate", back_populates="job", cascade="all, delete-orphan")


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)

    file_name = Column(String(255), nullable=False)
    raw_text = Column(Text, nullable=False)

    name = Column(String(255), nullable=True)
    skills = Column(JSON, default=list)
    experience_years = Column(Float, nullable=True)
    education = Column(String(255), nullable=True)
    projects = Column(JSON, default=list)
    certifications = Column(JSON, default=list)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    job = relationship("Job", back_populates="candidates")
    match = relationship("Match", back_populates="candidate", uselist=False, cascade="all, delete-orphan")


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False, unique=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)

    match_score = Column(Float, nullable=False)
    skill_score = Column(Float, nullable=True)
    experience_score = Column(Float, nullable=True)
    project_score = Column(Float, nullable=True)
    education_score = Column(Float, nullable=True)
    additional_skills_score = Column(Float, nullable=True)

    matching_skills = Column(JSON, default=list)
    missing_skills = Column(JSON, default=list)
    ai_explanation = Column(Text, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    candidate = relationship("Candidate", back_populates="match")