
from app.core.chroma_client import documents_collection
from app.services.embedding_service import generate_embeddings


def store_text_chunks(chunks, source="manual_test"):

    embeddings = generate_embeddings(chunks)

    ids = []
    metadatas = []

    for index in range(len(chunks)):
        ids.append(f"{source}_{index}")

        metadatas.append({
            "source": source,
            "chunk_index": index})

    documents_collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas)

    return len(chunks)
