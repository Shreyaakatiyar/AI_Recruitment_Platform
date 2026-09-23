from app.schemas.extraction_schemas import JobRequirementsExtraction
from app.services.llm_client import generate_structured

JOB_EXTRACTION_PROMPT = """You are an expert technical recruiter assistant.
Extract structured hiring requirements from the job description below.

Rules:
- required_skills: skills explicitly stated as mandatory/required
- preferred_skills: skills mentioned as "nice to have", "preferred", or "bonus"
- min_experience_years: minimum years of experience required, as a number (e.g. 3).
  If a range is given (e.g. "3-5 years"), use the lower bound. If not mentioned, leave null.
- required_education: the minimum education qualification mentioned (e.g. "Bachelor's in Computer Science").
  If not mentioned, leave null.
- Normalize skill names to their common form (e.g. "ReactJS" -> "React", "Node" -> "Node.js")
- Do not invent skills that are not mentioned in the text

Job Description:
\"\"\"
{job_text}
\"\"\"
"""


def extract_job_requirements(job_text: str) -> JobRequirementsExtraction:
    prompt = JOB_EXTRACTION_PROMPT.format(job_text=job_text)
    return generate_structured(prompt, JobRequirementsExtraction)