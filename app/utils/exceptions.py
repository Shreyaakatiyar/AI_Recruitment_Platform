class DocumentProcessingError(Exception):
    pass


class UnsupportedFileFormatError(DocumentProcessingError):
    def __init__(self, filename: str):
        self.filename = filename
        super().__init__(f"Unsupported file format for '{filename}'. Only PDF and DOCX are supported.")


class EmptyDocumentError(DocumentProcessingError):
    def __init__(self, filename: str):
        self.filename = filename
        super().__init__(f"'{filename}' contains no extractable text.")


class CorruptedDocumentError(DocumentProcessingError):
    def __init__(self, filename: str, reason: str = ""):
        self.filename = filename
        super().__init__(f"'{filename}' appears to be corrupted or unreadable. {reason}")

class LLMServiceError(Exception):
    pass

class EmbeddingServiceError(Exception):
    pass