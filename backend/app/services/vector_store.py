
from app.core.chroma_client import documents_collection
from app.services.embedding_service import generate_embeddings


def store_text_chunks(chunks, source="manual_test", chunk_metadata=None):

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

        if chunk_metadata:
            metadata.update(chunk_metadata[index])

        metadatas.append(metadata)

    # Replace older chunks belonging to this source
    documents_collection.delete(
        where={"source": source}
    )

    documents_collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(chunks)
