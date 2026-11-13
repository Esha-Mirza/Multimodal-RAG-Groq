
from app.core.chroma_client import documents_collection

print("ChromaDB initialized successfully!")
print("Collection name:", documents_collection.name)
print("Current documents:", documents_collection.count())
