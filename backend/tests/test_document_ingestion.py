
from pathlib import Path

from app.services.document_service import ingest_text_document
from app.core.chroma_client import documents_collection


# Locate the sample document
file_path = Path("data/uploads/sample_document.txt")

# Check whether the file exists
if not file_path.exists():
    raise FileNotFoundError("Sample document was not found.")

# Read the document
text = file_path.read_text(encoding="utf-8")

# Process and store the document
result = ingest_text_document(
    text=text,
    source=file_path.name
)

print("\nDOCUMENT INGESTION RESULTS")
print("--------------------------")

print("Source:", result["source"])
print("Total chunks:", result["total_chunks"])
print("Stored chunks:", result["stored_chunks"])

print("\nTotal records in ChromaDB:", documents_collection.count())
