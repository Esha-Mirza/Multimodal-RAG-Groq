
from app.services.document_service import ingest_pdf_document

pdf_path = input("Enter the PDF file path: ").strip().strip('"')

result = ingest_pdf_document(
    file_path=pdf_path,
    source="assignment_2_test.pdf"
)

print("\nPDF INGESTION RESULTS")
print("---------------------")

print("Source:", result["source"])
print("Total pages:", result["total_pages"])
print("Total chunks:", result["total_chunks"])
print("Stored chunks:", result["stored_chunks"])
