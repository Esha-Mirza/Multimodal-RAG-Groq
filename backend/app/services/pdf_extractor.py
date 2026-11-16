
from pathlib import Path
from pypdf import PdfReader


def extract_pdf_text(file_path):

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError("PDF file was not found.")

    reader = PdfReader(str(file_path))

    if reader.is_encrypted:
        raise ValueError("Encrypted PDF files are not supported.")

    extracted_pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        page_text = page.extract_text()

        if page_text and page_text.strip():

            extracted_pages.append({
                "page_number": page_number,
                "text": page_text.strip()})

    if not extracted_pages:
        raise ValueError(
            "No extractable text found. "
            "This PDF may contain scanned images and require OCR.")

    return extracted_pages
