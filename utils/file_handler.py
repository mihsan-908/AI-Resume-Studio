from pathlib import Path
from utils.pdf_reader import read_pdf
from utils.text_reader import read_text


SUPPORTED_EXTENSIONS = [".pdf", ".txt"]


def extract_resume_text(file_path: str) -> str:
    """
    Read a resume and return extracted text.

    Args:
        file_path (str): Resume path.

    Returns:
        str: Resume text.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError("Resume file not found.")

    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            "Unsupported file format. Please upload a PDF or TXT file."
        )

    if extension == ".pdf":
        return read_pdf(file_path)

    return read_text(file_path)