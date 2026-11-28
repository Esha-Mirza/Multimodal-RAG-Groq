
from app.core.chroma_client import documents_collection
from app.services.embedding_service import generate_embeddings


def store_text_chunks(
    chunks,
    source="manual_test",
    chunk_metadata=None,
    document_metadata=None
):

    if not chunks:
        return 0

    embeddings = generate_embeddings(chunks)

    ids = []
    metadatas = []

    for index in range(len(chunks)):

        ids.append(f"{source}_{index}")

        metadata = {
            "source": source,
            "chunk_index": index
        }

        if document_metadata:
            metadata.update(document_metadata)

        if chunk_metadata:
            metadata.update(chunk_metadata[index])

        metadatas.append(metadata)

    documents_collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(chunks)
