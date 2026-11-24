
from collections import Counter

from app.core.chroma_client import documents_collection


records = documents_collection.get(
    include=["metadatas"]
)

source_counts = Counter(
    metadata.get("source", "unknown")
    for metadata in records["metadatas"]
)

print("\nCHROMADB SOURCE AUDIT")
print("---------------------")
print("Total records:", len(records["ids"]))
print("Unique sources:", len(source_counts))

for source, count in sorted(source_counts.items()):

    print(f"{source}: {count} records")
