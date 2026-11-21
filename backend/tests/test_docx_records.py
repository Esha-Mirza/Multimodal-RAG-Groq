
from app.core.chroma_client import documents_collection


source = "docx_mixed_test"

print("\nDOCX DATABASE VERIFICATION")
print("--------------------------")

results = documents_collection.get(
    where={"source": source},
    include=["documents", "metadatas"]
)

print("Stored records:", len(results["ids"]))

for index in range(len(results["ids"])):

    print(f"\nRecord {index + 1}")
    print("ID:", results["ids"][index])
    print("Metadata:", results["metadatas"][index])
    print("Content:", results["documents"][index][:200])

print("\nVerification completed.")
