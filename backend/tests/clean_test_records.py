
from app.core.chroma_client import documents_collection


# Temporary test sources to remove
test_sources = [
    "test_document",
    "handbook_multimodal_test"
]

print("\nCLEANING TEST RECORDS")
print("---------------------")

for source in test_sources:

    results = documents_collection.get(
        where={"source": source}
    )

    record_ids = results["ids"]

    if record_ids:
        documents_collection.delete(ids=record_ids)
        print(f"Deleted {len(record_ids)} records from: {source}")

    else:
        print(f"No records found for: {source}")


# Display remaining records
print("\nREMAINING DATABASE RECORDS")
print("--------------------------")

print("Total records:", documents_collection.count())


# Display remaining document sources
remaining = documents_collection.get(
    include=["metadatas"]
)

remaining_sources = set()

for metadata in remaining["metadatas"]:
    remaining_sources.add(metadata["source"])

if remaining_sources:
    for source in sorted(remaining_sources):
        print("Source:", source)

else:
    print("No records remaining.")

print("\nCleanup completed.")
