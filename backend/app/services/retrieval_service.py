
from app.core.chroma_client import documents_collection
from app.services.embedding_service import generate_embeddings


def search_chunks(query, n_results=3, source=None):

    if not query or not query.strip():
        return []

    if source:

        matching_records = documents_collection.get(
            where={"source": source}
        )

        total_records = len(matching_records["ids"])

    else:
        total_records = documents_collection.count()

    if total_records == 0:
        return []

    query_embedding = generate_embeddings([query])

    query_arguments = {
        "query_embeddings": query_embedding,
        "n_results": min(n_results, total_records)
    }

    if source:
        query_arguments["where"] = {"source": source}

    results = documents_collection.query(**query_arguments)

    search_results = []

    for index in range(len(results["documents"][0])):

        search_results.append({
            "text": results["documents"][0][index],
            "metadata": results["metadatas"][0][index],
            "distance": results["distances"][0][index]
        })

    return search_results
