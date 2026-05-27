import fitz


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract text from a PDF file using PyMuPDF.

    Args:
        file_bytes: PDF file content in bytes.

    Returns:
        Extracted text as a string.
    """

    text = ""

    pdf_document = fitz.open(stream=file_bytes, filetype="pdf")

    for page in pdf_document:
        text += page.get_text()

    pdf_document.close()

    return text.strip()