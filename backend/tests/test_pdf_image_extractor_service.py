
from pathlib import Path

from app.services.pdf_extractor import extract_pdf_images


pdf_path = input("Enter PDF path: ").strip().strip('"')

output_dir = Path("data/test_extracted_images")

print("\nPDF IMAGE EXTRACTOR SERVICE TEST")
print("--------------------------------")

try:

    images = extract_pdf_images(
        file_path=pdf_path,
        output_dir=output_dir
    )

    print("\nTotal extracted images:", len(images))

    for image in images:

        print("\nPage:", image["page_number"])
        print("Image:", image["image_number"])
        print("Path:", image["image_path"])

except Exception as error:

    print("\nERROR:", error)
