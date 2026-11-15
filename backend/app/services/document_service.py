
from app.services.text_processor import split_text
from app.services.vector_store import store_text_chunks


def ingest_text_document(text, source):
    """
    Split a text document into chunks and store them
    in ChromaDB with their embeddings.
    """

    if not text or not text.strip():
        raise ValueError("The document is empty.")

    chunks = split_text(
        text,
        chunk_size=500,
        overlap=100)

    if not chunks:
        raise ValueError("No readable text was found.")

    stored_count = store_text_chunks(
        chunks,
        source=source)

    return {
        "source": source,
        "total_chunks": len(chunks),
        "stored_chunks": stored_count}
