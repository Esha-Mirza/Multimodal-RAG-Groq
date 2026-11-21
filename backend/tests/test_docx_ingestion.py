
from app.services.document_service import ingest_docx_document


docx_path = input("Enter DOCX file path: ").strip().strip('"')

source = "docx_mixed_test"

print("\nDOCX MIXED CONTENT INGESTION TEST")
print("--------------------------------")

try:

    result = ingest_docx_document(
        file_path=docx_path,
        source=source,
        analyze_images=False
    )

    print("\nINGESTION RESULTS")
    print("-----------------")

    print("Source:", result["source"])
    print("Text blocks:", result["total_text_blocks"])
    print("Extracted images:", result["total_images"])
    print("Skipped during extraction:", result["skipped_images"])
    print("Content blocks:", result["total_content_blocks"])
    print("Images processed:", result["images_processed"])
    print("Images skipped:", result["images_skipped"])
    print("Generated chunks:", result["total_chunks"])
    print("Stored chunks:", result["stored_chunks"])

    print("\nIMAGE ERRORS")

    for error in result["image_errors"]:
        print(error)

    print("\nMixed DOCX ingestion completed.")

except Exception as error:

    print("\nINGESTION ERROR:")
    print(type(error).__name__, error)
