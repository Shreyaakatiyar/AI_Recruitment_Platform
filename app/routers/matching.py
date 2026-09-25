from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.db_models import Job, Candidate, Match
from app.schemas.match_schemas import MatchResponse, RankingEntry, MatchBatchResult, FailedCandidateMatch
from app.services.matching_service import compute_and_save_match
from app.utils.exceptions import EmbeddingServiceError, LLMServiceError

router = APIRouter(tags=["Matching"])


@router.post("/match", response_model=MatchBatchResult)
def run_matching(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail=f"Job with id {job_id} not found")

    candidates = db.query(Candidate).filter(Candidate.job_id == job_id).all()
    if not candidates:
        raise HTTPException(status_code=400, detail="No candidates found for this job. Upload resumes first.")

    successful, failed = [], []
    for candidate in candidates:
        try:
            match = compute_and_save_match(db, job, candidate)
            successful.append(match)
        except (EmbeddingServiceError, LLMServiceError) as e:
            failed.append(FailedCandidateMatch(candidate_id=candidate.id, error=str(e)))

    return MatchBatchResult(successful_matches=successful, failed_candidates=failed)


@router.get("/ranking", response_model=list[RankingEntry])
def get_ranking(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail=f"Job with id {job_id} not found")

    matches = (
        db.query(Match)
        .filter(Match.job_id == job_id)
        .order_by(Match.match_score.desc())
        .all()
    )

    if not matches:
        raise HTTPException(status_code=404, detail="No matches found for this job. Run POST /match first.")

    return [
        RankingEntry(
            rank=idx,
            candidate_id=m.candidate_id,
            candidate_name=m.candidate.name,
            file_name=m.candidate.file_name,
            match_score=m.match_score,
            matching_skills=m.matching_skills,
            missing_skills=m.missing_skills,
        )
        for idx, m in enumerate(matches, start=1)
    ]