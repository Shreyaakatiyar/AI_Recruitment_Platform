from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.db_models import Candidate
from app.schemas.candidate_schemas import CandidateResponse

router = APIRouter(prefix="/candidates", tags=["Candidates"])


@router.get("", response_model=list[CandidateResponse])
def list_candidates(job_id: int | None = Query(default=None), db: Session = Depends(get_db)):
    query = db.query(Candidate)
    if job_id is not None:
        query = query.filter(Candidate.job_id == job_id)
    return query.all()


@router.get("/{candidate_id}", response_model=CandidateResponse)
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail=f"Candidate with id {candidate_id} not found")
    return candidate