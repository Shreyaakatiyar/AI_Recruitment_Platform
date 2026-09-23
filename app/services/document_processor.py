from io import BytesIO

from pypdf import PdfReader
from pypdf.errors import PdfReadError
from docx import Document as DocxDocument
from docx.opc.exceptions import PackageNotFoundError

from app.utils.exceptions import (
    UnsupportedFileFormatError,
    EmptyDocumentError,
    CorruptedDocumentError,
)

SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


def _get_extension(filename: str) -> str:
    if "." not in filename:
        return ""
    return "." + filename.rsplit(".", 1)[-1].lower()


def extract_text_from_pdf(file_bytes: bytes, filename: str) -> str:
    try:
        reader = PdfReader(BytesIO(file_bytes))
        text_parts = [page.extract_text() or "" for page in reader.pages]
        text = "\n".join(text_parts).strip()
    except PdfReadError as e:
        raise CorruptedDocumentError(filename, str(e))
    except Exception as e:
        raise CorruptedDocumentError(filename, str(e))

    if not text:
        raise EmptyDocumentError(filename)
    return text


def extract_text_from_docx(file_bytes: bytes, filename: str) -> str:
    try:
        doc = DocxDocument(BytesIO(file_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        text = "\n".join(paragraphs).strip()
    except PackageNotFoundError as e:
        raise CorruptedDocumentError(filename, str(e))
    except Exception as e:
        raise CorruptedDocumentError(filename, str(e))

    if not text:
        raise EmptyDocumentError(filename)
    return text


def extract_text(file_bytes: bytes, filename: str) -> str:
    extension = _get_extension(filename)

    if extension not in SUPPORTED_EXTENSIONS:
        raise UnsupportedFileFormatError(filename)

    if not file_bytes or len(file_bytes) == 0:
        raise EmptyDocumentError(filename)

    if extension == ".pdf":
        return extract_text_from_pdf(file_bytes, filename)
    elif extension == ".docx":
        return extract_text_from_docx(file_bytes, filename)