
from app.core.chroma_client import documents_collection

results = documents_collection.get(
    where={"source": "assignment_2_test.pdf"},
    include=["documents", "metadatas"])

print("\nPDF STORED METADATA")
print("-------------------")

for document, metadata in zip(
    results["documents"],
    results["metadatas"]):

    print("\nPage:", metadata["page_number"])
    print("Chunk:", metadata["chunk_index"])
    print("Text:", document[:200])
