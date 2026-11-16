
from app.core.chroma_client import documents_collection

# Find records created by our earlier manual test
results = documents_collection.get(
    where={"source": "test_document"}
)

# Get their IDs
record_ids = results["ids"]

# Delete temporary test records
if record_ids:
    documents_collection.delete(ids=record_ids)
    print("Temporary test records deleted:", len(record_ids))
else:
    print("No temporary test records found.")

# Display remaining records
print("Remaining records:", documents_collection.count())

# Display remaining document sources
remaining = documents_collection.get(
    include=["metadatas"]
)

for metadata in remaining["metadatas"]:
    print("Source:", metadata["source"])
