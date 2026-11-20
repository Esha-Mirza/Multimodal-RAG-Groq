
from pathlib import Path
from pypdf import PdfReader

from app.services.text_processor import split_text
from app.services.pdf_extractor import (
    extract_pdf_text,
    extract_pdf_images
)


def ingest_text_document(text, source):

    if not text or not text.strip():
        raise ValueError("The document is empty.")

    chunks = split_text(
        text,
        chunk_size=500,
        overlap=100
    )

    if not chunks:
        raise ValueError("No readable text was found.")

    from app.services.vector_store import store_text_chunks

    stored_count = store_text_chunks(
        chunks,
        source=source
    )

    return {
        "source": source,
        "total_chunks": len(chunks),
        "stored_chunks": stored_count
    }


def extract_pdf_content(file_path, source):

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError("PDF file was not found.")

    reader = PdfReader(str(file_path))

    if reader.is_encrypted:
        raise ValueError("Encrypted PDF files are not supported.")

    pages = extract_pdf_text(file_path)

    image_output_dir = (
        Path(__file__).resolve().parents[2]
        / "data"
        / "extracted_images"
        / Path(source).stem
    )

    images = extract_pdf_images(
        file_path=file_path,
        output_dir=image_output_dir
    )

    return {
        "pages": pages,
        "images": images,
        "total_pages": len(reader.pages),
        "total_text_pages": len(pages),
        "total_images": len(images)
    }


def ingest_pdf_document(file_path, source):

    extracted_content = extract_pdf_content(
        file_path=file_path,
        source=source
    )

    pages = extracted_content["pages"]
    images = extracted_content["images"]

    all_chunks = []
    chunk_metadata = []

    # Process extracted PDF text
    for page in pages:

        page_chunks = split_text(
            page["text"],
            chunk_size=500,
            overlap=100
        )

        for chunk in page_chunks:

            all_chunks.append(chunk)

            chunk_metadata.append({
                "page_number": page["page_number"],
                "content_type": "text"
            })

    # Process extracted images using Groq Vision
    if images:

        from app.services.image_understanding_service import understand_image

        for image in images:

            print(
                f"Analyzing image {image['image_number']} "
                f"on page {image['page_number']}..."
            )

            image_description = understand_image(
                image["image_path"]
            )

            image_chunks = split_text(
                image_description,
                chunk_size=500,
                overlap=100
            )

            for chunk in image_chunks:

                all_chunks.append(chunk)

                chunk_metadata.append({
                    "page_number": image["page_number"],
                    "image_number": image["image_number"],
                    "content_type": "image"
                })

    if not all_chunks:
        raise ValueError(
            "No readable text or processable images were found in the PDF."
        )

    from app.services.vector_store import store_text_chunks

    stored_count = store_text_chunks(
        chunks=all_chunks,
        source=source,
        chunk_metadata=chunk_metadata
    )

    return {
        "source": source,
        "total_pages": extracted_content["total_pages"],
        "total_images": extracted_content["total_images"],
        "total_chunks": len(all_chunks),
        "stored_chunks": stored_count
    }
