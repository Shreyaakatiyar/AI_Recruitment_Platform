from unittest.mock import patch

from app.schemas.extraction_schemas import JobRequirementsExtraction, CandidateProfileExtraction
from app.utils.exceptions import UnsupportedFileFormatError


def _create_job(client):
    fake = JobRequirementsExtraction(required_skills=["Python"], preferred_skills=[])
    with patch("app.routers.jobs.extract_job_requirements", return_value=fake):
        response = client.post("/jobs", json={
            "title": "Backend Developer",
            "raw_text": "We need a backend developer with Python experience.",
        })
    return response.json()["id"]


def test_upload_resume_success(client):
    job_id = _create_job(client)
    fake_profile = CandidateProfileExtraction(name="Jane Doe", skills=["Python", "SQL"], experience_years=3)

    with patch("app.routers.resumes.extract_text", return_value="Resume text with Python and SQL."), \
         patch("app.routers.resumes.extract_candidate_profile", return_value=fake_profile):
        response = client.post(
            "/resumes",
            data={"job_id": job_id},
            files={"file": ("resume.pdf", b"%PDF-1.4 fake content", "application/pdf")},
        )
    assert response.status_code == 201
    assert response.json()["name"] == "Jane Doe"


def test_upload_resume_missing_job_returns_404(client):
    response = client.post(
        "/resumes",
        data={"job_id": 9999},
        files={"file": ("resume.pdf", b"content", "application/pdf")},
    )
    assert response.status_code == 404


def test_upload_resume_unsupported_format_returns_400(client):
    job_id = _create_job(client)
    with patch("app.routers.resumes.extract_text", side_effect=UnsupportedFileFormatError("resume.txt")):
        response = client.post(
            "/resumes",
            data={"job_id": job_id},
            files={"file": ("resume.txt", b"content", "text/plain")},
        )
    assert response.status_code == 400