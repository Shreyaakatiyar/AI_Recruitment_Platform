from unittest.mock import patch

from app.schemas.extraction_schemas import JobRequirementsExtraction
from app.utils.exceptions import LLMServiceError


def test_create_job_success(client):
    fake = JobRequirementsExtraction(
        required_skills=["Python", "FastAPI"],
        preferred_skills=["Docker"],
        min_experience_years=2,
        required_education="Bachelor's in Computer Science",
    )
    with patch("app.routers.jobs.extract_job_requirements", return_value=fake):
        response = client.post("/jobs", json={
            "title": "Backend Developer",
            "raw_text": "We need a backend developer with Python and FastAPI experience.",
        })
    assert response.status_code == 201
    assert response.json()["required_skills"] == ["Python", "FastAPI"]


def test_create_job_invalid_input_too_short(client):
    response = client.post("/jobs", json={"title": "X", "raw_text": "too short"})
    assert response.status_code == 422  


def test_create_job_llm_failure_returns_502(client):
    with patch("app.routers.jobs.extract_job_requirements", side_effect=LLMServiceError("boom")):
        response = client.post("/jobs", json={
            "title": "Backend Developer",
            "raw_text": "We need a backend developer with Python experience.",
        })
    assert response.status_code == 502