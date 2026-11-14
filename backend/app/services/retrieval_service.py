
from app.core.chroma_client import documents_collection
from app.services.embedding_service import generate_embeddings


def search_chunks(query, n_results=3):

    if documents_collection.count() == 0:
        return []

    # Convert the user's question into an embedding
    query_embedding = generate_embeddings([query])

    # Search ChromaDB using the query embedding
    results = documents_collection.query(
        query_embeddings=query_embedding,
        n_results=min(n_results, documents_collection.count())
    )

    search_results = []

    for index in range(len(results["documents"][0])):

        search_results.append({
            "text": results["documents"][0][index],
            "metadata": results["metadatas"][0][index],
            "distance": results["distances"][0][index]})

    return search_results
