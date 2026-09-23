import pytest
from app.services.document_processor import extract_text
from app.utils.exceptions import UnsupportedFileFormatError, EmptyDocumentError


def test_rejects_unsupported_format():
    with pytest.raises(UnsupportedFileFormatError):
        extract_text(b"some content", "resume.txt")


def test_rejects_empty_file():
    with pytest.raises(EmptyDocumentError):
        extract_text(b"", "resume.pdf")