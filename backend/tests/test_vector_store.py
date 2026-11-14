
from app.services.vector_store import store_text_chunks
from app.core.chroma_client import documents_collection


sample_chunks = [
    "Artificial intelligence enables machines to perform intelligent tasks.",
    "Machine learning allows computers to learn patterns from data.",
    "Pakistan is located in South Asia."
]

stored_count = store_text_chunks(
    sample_chunks,
    source="test_document"
)

print("Stored chunks:", stored_count)
print("Total records in ChromaDB:", documents_collection.count())

print("\nStored documents:")

results = documents_collection.get(
    ids=[
        "test_document_0",
        "test_document_1",
        "test_document_2"
    ]
)

for document in results["documents"]:
    print(document)
