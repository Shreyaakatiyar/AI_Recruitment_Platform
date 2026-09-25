from unittest.mock import patch

from app.schemas.extraction_schemas import JobRequirementsExtraction


def _create_job(client):
    fake = JobRequirementsExtraction(required_skills=[], preferred_skills=[])
    with patch("app.routers.jobs.extract_job_requirements", return_value=fake):
        response = client.post("/jobs", json={
            "title": "Backend Developer",
            "raw_text": "We need a backend developer with Python experience.",
        })
    return response.json()["id"]


def test_match_job_not_found_returns_404(client):
    response = client.post("/match?job_id=9999")
    assert response.status_code == 404


def test_match_no_candidates_returns_400(client):
    job_id = _create_job(client)
    response = client.post(f"/match?job_id={job_id}")
    assert response.status_code == 400


def test_ranking_before_matching_returns_404(client):
    job_id = _create_job(client)
    response = client.get(f"/ranking?job_id={job_id}")
    assert response.status_code == 404