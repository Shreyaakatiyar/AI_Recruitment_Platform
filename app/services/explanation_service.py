from google.genai import types

from app.services.gemini_client import client
from app.utils.exceptions import LLMServiceError

EXPLANATION_MODEL = "gemini-3.5-flash-lite"

EXPLANATION_PROMPT = """You are a technical recruiter assistant. Write a short, professional
explanation (3-5 sentences) of this candidate's suitability for the role, based ONLY on
the data below. Be specific and factual — do not invent skills or experience not listed.

Job Title: {job_title}
Overall Match Score: {match_score}/100

Score Breakdown:
- Required Skills Match: {skill_score}/100
- Relevant Experience: {experience_score}/100
- Projects: {project_score}/100
- Education: {education_score}/100

Matching Skills: {matching_skills}
Missing Skills: {missing_skills}

Write the explanation covering: (1) overall fit summary, (2) key strengths, (3) notable gaps
or risks, in a neutral, factual tone a recruiter can act on.
"""


def generate_match_explanation(
    job_title: str,
    match_score: float,
    skill_score: float,
    experience_score: float,
    project_score: float,
    education_score: float,
    matching_skills: list[str],
    missing_skills: list[str],
) -> str:
    prompt = EXPLANATION_PROMPT.format(
        job_title=job_title,
        match_score=match_score,
        skill_score=skill_score,
        experience_score=experience_score,
        project_score=project_score,
        education_score=education_score,
        matching_skills=", ".join(matching_skills) if matching_skills else "None",
        missing_skills=", ".join(missing_skills) if missing_skills else "None",
    )

    try:
        response = client.models.generate_content(
            model=EXPLANATION_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.4),
        )
    except Exception as e:
        raise LLMServiceError(f"Gemini explanation generation failed: {e}")

    if not response.text:
        raise LLMServiceError("Gemini returned an empty explanation.")

    return response.text.strip()