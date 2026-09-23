from sqlalchemy.orm import Session

from app.config import settings
from app.models.db_models import Job, Candidate, Match
from app.services.scoring_service import (
    compute_skill_match,
    compute_experience_score,
    compute_project_score,
    compute_education_score,
)


def compute_and_save_match(db: Session, job: Job, candidate: Candidate) -> Match:
    skill_score, matching_skills, missing_skills = compute_skill_match(job.required_skills, candidate.skills)
    additional_skills_score, _, _ = compute_skill_match(job.preferred_skills, candidate.skills)
    experience_score = compute_experience_score(job.min_experience_years, candidate.experience_years)
    project_score = compute_project_score(job.raw_text, candidate.projects, candidate.raw_text)
    education_score = compute_education_score(job.required_education, candidate.education)

    final_score = (
        settings.weight_required_skills * skill_score
        + settings.weight_experience * experience_score
        + settings.weight_projects * project_score
        + settings.weight_education * education_score
        + settings.weight_additional_skills * additional_skills_score
    ) * 100

    match = db.query(Match).filter(Match.candidate_id == candidate.id).first()
    if match is None:
        match = Match(candidate_id=candidate.id, job_id=job.id)
        db.add(match)

    match.match_score = round(final_score, 2)
    match.skill_score = round(skill_score * 100, 2)
    match.experience_score = round(experience_score * 100, 2)
    match.project_score = round(project_score * 100, 2)
    match.education_score = round(education_score * 100, 2)
    match.additional_skills_score = round(additional_skills_score * 100, 2)
    match.matching_skills = matching_skills
    match.missing_skills = missing_skills

    db.commit()
    db.refresh(match)
    return match