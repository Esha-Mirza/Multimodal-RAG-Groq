
from app.core.chroma_client import documents_collection
from app.services.embedding_service import generate_embeddings


question = "What are the deliverables required for Assignment 2?"

query_embedding = generate_embeddings([question])

results = documents_collection.query(
    query_embeddings=query_embedding,
    n_results=5,
    where={"source": "assignment_2_test.pdf"},
    include=["documents", "metadatas", "distances"]
)

print("\nPDF RETRIEVAL RESULTS")
print("---------------------")

for index in range(len(results["documents"][0])):

    print("\nResult:", index + 1)
    print("Distance:", results["distances"][0][index])
    print("Page:", results["metadatas"][0][index]["page_number"])
    print("Chunk:", results["metadatas"][0][index]["chunk_index"])
    print("Text:", results["documents"][0][index][:300])
