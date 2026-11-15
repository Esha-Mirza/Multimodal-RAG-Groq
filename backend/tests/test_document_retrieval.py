
from app.services.retrieval_service import search_chunks


question = "What does computer vision allow machines to do?"

results = search_chunks(
    query=question,
    n_results=3
)

print("\nUSER QUESTION:")
print(question)

print("\nRETRIEVED DOCUMENT CHUNKS:")

for result in results:

    print("\nSource:", result["metadata"]["source"])
    print("Chunk:", result["metadata"]["chunk_index"])
    print("Text:", result["text"])
    print("Distance:", result["distance"])
