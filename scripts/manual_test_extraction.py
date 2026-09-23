import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.document_processor import extract_text
from app.services.candidate_extraction_service import extract_candidate_profile


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/manual_test_extraction.py <path_to_resume>")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    file_bytes = file_path.read_bytes()

    print(f"Extracting text from {file_path.name}...")
    raw_text = extract_text(file_bytes, file_path.name)
    print(f"Extracted {len(raw_text)} characters.\n")

    print("Calling Gemini for structured extraction...")
    profile = extract_candidate_profile(raw_text)
    print("\n--- Extracted Candidate Profile ---")
    print(profile.model_dump_json(indent=2))


if __name__ == "__main__":
    main()