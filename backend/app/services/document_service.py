
from pathlib import Path

from app.services.text_processor import split_text
from app.services.vector_store import store_text_chunks
from app.services.pdf_extractor import extract_pdf_text


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

    all_chunks = []
    chunk_metadata = []

    for page in pages:

        page_chunks = split_text(
            page["text"],
            chunk_size=500,
            overlap=100
        )

        for chunk in page_chunks:

            all_chunks.append(chunk)

            chunk_metadata.append({
                "page_number": page["page_number"]
            })

    if not all_chunks:
        raise ValueError("No readable text was found in the PDF.")

    stored_count = store_text_chunks(
        chunks=all_chunks,
        source=source,
        chunk_metadata=chunk_metadata
    )

    return {
        "source": source,
        "total_pages": len(pages),
        "total_chunks": len(all_chunks),
        "stored_chunks": stored_count
    }
