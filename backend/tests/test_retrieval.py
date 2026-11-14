
from app.services.retrieval_service import search_chunks


question = "How do computers learn patterns from data?"

results = search_chunks(
    query=question,
    n_results=3)

print("User Question:", question)

print("\nRetrieved Results:")

for result in results:

    print("\nText:", result["text"])
    print("Source:", result["metadata"]["source"])
    print("Distance:", result["distance"])
