
from pathlib import Path

from app.services.text_processor import split_text
from app.services.vector_store import store_text_chunks
from app.services.pdf_extractor import (
    extract_pdf_text,
    extract_pdf_images
)
from app.services.image_understanding_service import understand_image


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

    stored_count = store_text_chunks(
        chunks,
        source=source
    )

    return {
        "source": source,
        "total_chunks": len(chunks),
        "stored_chunks": stored_count
    }


def ingest_pdf_document(file_path, source):

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

    all_chunks = []
    chunk_metadata = []

    # Process text extracted from PDF pages
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

    # Process images using Groq Vision
    for image in images:

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

    stored_count = store_text_chunks(
        chunks=all_chunks,
        source=source,
        chunk_metadata=chunk_metadata
    )

    total_pages = max(
        [page["page_number"] for page in pages]
        + [image["page_number"] for image in images],
        default=0
    )

    return {
        "source": source,
        "total_pages": total_pages,
        "total_images": len(images),
        "total_chunks": len(all_chunks),
        "stored_chunks": stored_count
    }
