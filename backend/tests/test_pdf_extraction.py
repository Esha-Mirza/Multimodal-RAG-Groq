
from pathlib import Path
from app.services.pdf_extractor import extract_pdf_text

pdf_path = input("Enter the PDF file path: ").strip().strip('"')

pages = extract_pdf_text(pdf_path)

print("\nPDF EXTRACTION RESULTS")
print("----------------------")

print("Total pages extracted:", len(pages))

for page in pages:

    print("\nPage:", page["page_number"])
    print("Extracted text:")
    print(page["text"][:500])
