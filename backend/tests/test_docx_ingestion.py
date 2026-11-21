
from app.services.document_service import ingest_docx_document


docx_path = input("Enter DOCX file path: ").strip().strip('"')

source = "docx_ingestion_test"

print("\nDOCX INGESTION TEST")
print("-------------------")

try:

    result = ingest_docx_document(
        file_path=docx_path,
        source=source
    )

    print("\nINGESTION RESULTS")
    print("-----------------")

    print("Source:", result["source"])
    print("Text blocks:", result["total_text_blocks"])
    print("Images:", result["total_images"])
    print("Skipped images:", result["skipped_images"])
    print("Content blocks:", result["total_content_blocks"])
    print("Generated chunks:", result["total_chunks"])
    print("Stored chunks:", result["stored_chunks"])

    print("\nDOCX ingestion completed.")

except Exception as error:

    print("\nINGESTION ERROR:")
    print(type(error).__name__, error)
