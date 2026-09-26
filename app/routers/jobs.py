from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.db_models import Job
from app.schemas.job_schemas import JobCreate, JobResponse
from app.services.job_extraction_service import extract_job_requirements
from app.utils.exceptions import LLMServiceError

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("", response_model=JobResponse, status_code=201)
def create_job(payload: JobCreate, db: Session = Depends(get_db)):
    try:
        extracted = extract_job_requirements(payload.raw_text)
    except LLMServiceError as e:
        raise HTTPException(status_code=502, detail=str(e))

    job = Job(
        title=payload.title,
        raw_text=payload.raw_text,
        required_skills=extracted.required_skills,
        preferred_skills=extracted.preferred_skills,
        min_experience_years=extracted.min_experience_years,
        required_education=extracted.required_education,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

@router.get("", response_model=list[JobResponse])
def list_jobs(db: Session = Depends(get_db)):
    return db.query(Job).all()


@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail=f"Job with id {job_id} not found")
    return job