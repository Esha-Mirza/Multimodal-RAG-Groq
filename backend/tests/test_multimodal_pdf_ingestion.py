
from app.services.document_service import ingest_pdf_document


pdf_path = input("Enter PDF path: ").strip().strip('"')

print("\nMULTIMODAL PDF INGESTION TEST")
print("-----------------------------")

try:

    result = ingest_pdf_document(
        file_path=pdf_path,
        source="handbook_multimodal_test"
    )

    print("\nINGESTION RESULTS")

    for key, value in result.items():
        print(f"{key}: {value}")

except Exception as error:

    print("\nERROR:")
    print(error)
