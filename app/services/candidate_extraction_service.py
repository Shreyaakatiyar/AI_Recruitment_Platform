from app.schemas.extraction_schemas import CandidateProfileExtraction
from app.services.llm_client import generate_structured

CANDIDATE_EXTRACTION_PROMPT = """You are an expert resume parser.
Extract a structured candidate profile from the resume text below.

Rules:
- name: the candidate's full name
- skills: all technical skills mentioned (languages, frameworks, tools, platforms)
- experience_years: total professional experience in years, as a number. Estimate from
  work history dates if not explicitly stated. If it truly cannot be determined, leave null.
- education: highest qualification mentioned (e.g. "B.Tech Computer Science")
- projects: short names/titles of projects mentioned, not full descriptions
- certifications: any certifications listed
- Normalize skill names to their common form (e.g. "ReactJS" -> "React")
- Do not invent information that is not present in the text

Resume Text:
\"\"\"
{resume_text}
\"\"\"
"""


def extract_candidate_profile(resume_text: str) -> CandidateProfileExtraction:
    prompt = CANDIDATE_EXTRACTION_PROMPT.format(resume_text=resume_text)
    return generate_structured(prompt, CandidateProfileExtraction)