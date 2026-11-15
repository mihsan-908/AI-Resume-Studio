import pdfplumber


def read_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        str: Extracted text.
    """

    extracted_text = ""

    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()

                if text:
                    extracted_text += text + "\n"

    except Exception as e:
        raise Exception(f"Error reading PDF: {e}")

    return extracted_text.strip()