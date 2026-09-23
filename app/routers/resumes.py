from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.db_models import Job, Candidate
from app.schemas.candidate_schemas import CandidateResponse
from app.services.document_processor import extract_text
from app.services.candidate_extraction_service import extract_candidate_profile
from app.utils.exceptions import DocumentProcessingError, LLMServiceError

router = APIRouter(prefix="/resumes", tags=["Resumes"])


@router.post("", response_model=CandidateResponse, status_code=201)
async def upload_resume(
    job_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail=f"Job with id {job_id} not found")

    file_bytes = await file.read()

    try:
        raw_text = extract_text(file_bytes, file.filename)
    except DocumentProcessingError as e:
        raise HTTPException(status_code=400, detail=str(e))

    try:
        extracted = extract_candidate_profile(raw_text)
    except LLMServiceError as e:
        raise HTTPException(status_code=502, detail=str(e))

    candidate = Candidate(
        job_id=job_id,
        file_name=file.filename,
        raw_text=raw_text,
        name=extracted.name,
        skills=extracted.skills,
        experience_years=extracted.experience_years,
        education=extracted.education,
        projects=extracted.projects,
        certifications=extracted.certifications,
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return candidate