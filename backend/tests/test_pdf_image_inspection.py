
from pathlib import Path
from pypdf import PdfReader


pdf_path = input("Enter the PDF file path: ").strip().strip('"')

pdf_path = Path(pdf_path)

if not pdf_path.exists():
    print("PDF file not found.")
    exit()

reader = PdfReader(str(pdf_path))

print("\nPDF IMAGE INSPECTION")
print("--------------------")

print("Total pages:", len(reader.pages))

total_images = 0

for page_number, page in enumerate(reader.pages, start=1):

    images = page.images

    print(f"\nPage {page_number}")
    print("Images found:", len(images))

    for image_number, image in enumerate(images, start=1):

        total_images += 1

        print(f"\nImage {image_number}")
        print("Image name:", image.name)
        print("Image format:", Path(image.name).suffix)

        try:
            print("Image dimensions:", image.image.size)
        except Exception:
            print("Image dimensions: Could not determine")

print("\n--------------------")
print("Total embedded images:", total_images)
