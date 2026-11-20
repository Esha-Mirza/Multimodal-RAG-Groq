
from app.services.document_service import extract_pdf_content


pdf_path = input("Enter PDF path: ").strip().strip('"')

print("\nPDF CONTENT EXTRACTION TEST")
print("---------------------------")

try:

    result = extract_pdf_content(
        file_path=pdf_path,
        source="pdf_extraction_test"
    )

    print("\nEXTRACTION RESULTS")
    print("------------------")

    print("Total pages:", result["total_pages"])
    print("Pages with selectable text:", result["total_text_pages"])
    print("Embedded images:", result["total_images"])

    print("\nEXTRACTED TEXT PREVIEW")
    print("----------------------")

    for page in result["pages"][:3]:

        print("\nPage:", page["page_number"])
        print(page["text"][:300])

    print("\nEXTRACTED IMAGE DETAILS")
    print("-----------------------")

    for image in result["images"][:10]:

        print(
            "Page:", image["page_number"],
            "| Image:", image["image_number"],
            "| Path:", image["image_path"]
        )

    print("\nExtraction completed successfully.")

except Exception as error:

    print("\nERROR:")
    print(error)
