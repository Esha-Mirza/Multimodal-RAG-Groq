
from app.core.chroma_client import documents_collection


source = "handbook_multimodal_test"

results = documents_collection.get(
    where={"source": source},
    include=["documents", "metadatas"]
)

text_count = 0
image_count = 0

print("\nMULTIMODAL STORAGE VERIFICATION")
print("--------------------------------")

for metadata in results["metadatas"]:

    if metadata["content_type"] == "text":
        text_count += 1

    elif metadata["content_type"] == "image":
        image_count += 1

print("Total stored records:", len(results["ids"]))
print("Text chunks:", text_count)
print("Image-derived chunks:", image_count)

print("\nSAMPLE IMAGE RECORDS")
print("--------------------")

for index, metadata in enumerate(results["metadatas"]):

    if metadata["content_type"] == "image":

        print("\nPage:", metadata["page_number"])
        print("Image:", metadata["image_number"])
        print("Content:", results["documents"][index][:300])

        break
