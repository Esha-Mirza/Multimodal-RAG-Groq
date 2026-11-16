
from app.core.chroma_client import documents_collection
from app.services.embedding_service import generate_embeddings


def search_chunks(query, n_results=3):

    if not query or not query.strip():
        return []

    total_records = documents_collection.count()

    if total_records == 0:
        return []

    query_embedding = generate_embeddings([query])

    results = documents_collection.query(
        query_embeddings=query_embedding,
        n_results=min(n_results, total_records)
    )

    search_results = []

    for index in range(len(results["documents"][0])):

        search_results.append({
            "text": results["documents"][0][index],
            "metadata": results["metadatas"][0][index],
            "distance": results["distances"][0][index]
        })

    return search_results
