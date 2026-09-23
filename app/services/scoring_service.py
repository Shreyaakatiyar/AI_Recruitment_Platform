from app.services.embedding_service import get_embedding
from app.utils.math_utils import cosine_similarity

SKILL_MATCH_THRESHOLD = 0.72
EDUCATION_STRONG_MATCH_THRESHOLD = 0.80
EDUCATION_PARTIAL_MATCH_THRESHOLD = 0.60


def _is_semantic_match(target_skill: str, candidate_skills: list[str]) -> bool:
    target_lower = target_skill.lower()
    for cand_skill in candidate_skills:
        cand_lower = cand_skill.lower()
        if target_lower == cand_lower or target_lower in cand_lower or cand_lower in target_lower:
            return True

    if not candidate_skills:
        return False

    target_embedding = get_embedding(target_skill)
    for cand_skill in candidate_skills:
        similarity = cosine_similarity(target_embedding, get_embedding(cand_skill))
        if similarity >= SKILL_MATCH_THRESHOLD:
            return True

    return False


def compute_skill_match(target_skills: list[str], candidate_skills: list[str]) -> tuple[float, list[str], list[str]]:
    if not target_skills:
        return 1.0, [], []  

    matching, missing = [], []
    for skill in target_skills:
        if _is_semantic_match(skill, candidate_skills):
            matching.append(skill)
        else:
            missing.append(skill)

    score = len(matching) / len(target_skills)
    return score, matching, missing


def compute_experience_score(min_experience_years: float | None, candidate_experience_years: float | None) -> float:
    if min_experience_years is None or min_experience_years <= 0:
        return 1.0
    if candidate_experience_years is None:
        return 0.0
    return min(candidate_experience_years / min_experience_years, 1.0)


def compute_education_score(required_education: str | None, candidate_education: str | None) -> float:
    if not required_education:
        return 1.0
    if not candidate_education:
        return 0.0

    similarity = cosine_similarity(get_embedding(required_education), get_embedding(candidate_education))
    if similarity >= EDUCATION_STRONG_MATCH_THRESHOLD:
        return 1.0
    elif similarity >= EDUCATION_PARTIAL_MATCH_THRESHOLD:
        return 0.6
    return 0.0


def compute_project_score(job_raw_text: str, candidate_projects: list[str], candidate_raw_text: str) -> float:
    reference_text = " ".join(candidate_projects) if candidate_projects else candidate_raw_text
    if not reference_text.strip():
        return 0.0

    similarity = cosine_similarity(get_embedding(job_raw_text), get_embedding(reference_text))
    return max(0.0, min((similarity - 0.3) / 0.5, 1.0))