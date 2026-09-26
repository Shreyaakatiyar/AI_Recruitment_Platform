# Test Cases

Automated tests live in `tests/` and run via `pytest tests/ -v`. This document maps each
required scenario from the assignment to how it's covered.

| # | Scenario | Covered By | Expected Result |
|---|---|---|---|
| 1 | Valid resume | `test_upload_resume_success` + manual test with real PDF/DOCX | 201, structured profile returned |
| 2 | Invalid resume (unsupported format) | `test_upload_resume_unsupported_format_returns_400` | 400, `UnsupportedFileFormatError` message |
| 3 | Resume with incomplete information | Manual test: resume with no education section | LLM returns `null` for missing fields, no crash |
| 4 | Different resume formats (PDF vs DOCX) | Manual test with one of each | Both extract successfully |
| 5 | Candidate with high skill match | Manual test: resume closely matching JD | High `match_score`, few/no missing skills |
| 6 | Candidate with low skill match | Manual test: resume unrelated to JD | Low `match_score`, many missing skills |
| 7 | Candidate with similar but differently worded skills | Manual test: JD says "Python backend development", resume says "Developed REST APIs using Python and FastAPI" | Skill counted as matching via embedding similarity, not exact text |
| 8 | Multiple candidates | Manual test: 3+ resumes against one job | `GET /ranking` returns all, sorted descending |
| 9 | No matching candidates | Manual test: JD with a required skill no candidate has | Skill appears in every candidate's `missing_skills` |
| 10 | LLM/API failure | `test_create_job_llm_failure_returns_502` | 502, no crash, no raw traceback exposed |
| 11 | Empty document | Manual test: 0-byte PDF | 400, `EmptyDocumentError` message |
| 12 | Corrupted document | Manual test: rename a `.jpg` to `.pdf` and upload | 400, `CorruptedDocumentError` message |
| 13 | Missing Job Description | `test_create_job_invalid_input_too_short` | 422, Pydantic validation error |
| 14 | Missing candidate information | Manual test: resume that's just a name and one line | LLM extracts what's available, nulls for the rest, no crash |
| 15 | Job not found | `test_match_job_not_found_returns_404`, `test_upload_resume_missing_job_returns_404` | 404 |
| 16 | No candidates uploaded yet | `test_match_no_candidates_returns_400` | 400 |
| 17 | Ranking requested before matching | `test_ranking_before_matching_returns_404` | 404 |
| 18 | Multiple candidate processing failures | Batch matching design (see `matching_service.py` + `MatchBatchResult`) | One candidate's failure doesn't block others; reported separately in `failed_candidates` |

## Running the automated suite
\`\`\`bash
pytest tests/ -v
\`\`\`