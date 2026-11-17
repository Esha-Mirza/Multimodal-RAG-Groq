
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
                "text": page_text.strip()
            })


    return extracted_pages


def extract_pdf_images(file_path, output_dir):

    file_path = Path(file_path)
    output_dir = Path(output_dir)

    if not file_path.exists():
        raise FileNotFoundError("PDF file was not found.")

    reader = PdfReader(str(file_path))

    if reader.is_encrypted:
        raise ValueError("Encrypted PDF files are not supported.")

    extracted_images = []

    for page_number, page in enumerate(reader.pages, start=1):

        for image_number, image in enumerate(page.images, start=1):

            image_extension = Path(image.name).suffix.lower()

            if image_extension not in [".jpg", ".jpeg", ".png"]:
                continue

            page_dir = output_dir / f"page_{page_number}"
            page_dir.mkdir(parents=True, exist_ok=True)

            image_filename = (
                f"image_{image_number}{image_extension}"
            )

            image_path = page_dir / image_filename

            image_path.write_bytes(image.data)

            extracted_images.append({
                "page_number": page_number,
                "image_number": image_number,
                "image_path": str(image_path)
            })

    return extracted_images
