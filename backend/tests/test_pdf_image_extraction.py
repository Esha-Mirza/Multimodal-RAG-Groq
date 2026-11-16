
from pathlib import Path
from pypdf import PdfReader


pdf_path = input("Enter the PDF file path: ").strip().strip('"')

pdf_path = Path(pdf_path)

if not pdf_path.exists():
    print("PDF file not found.")
    exit()


output_dir = Path("data/extracted_images")

output_dir.mkdir(
    parents=True,
    exist_ok=True
)

reader = PdfReader(str(pdf_path))

total_images = 0

print("\nPDF IMAGE EXTRACTION")
print("--------------------")

for page_number, page in enumerate(reader.pages, start=1):

    images = page.images

    if len(images) == 0:
        continue

    print(f"\nPage {page_number}")

    for image_number, image in enumerate(images, start=1):

        image_extension = Path(image.name).suffix.lower()

        image_filename = (
            f"page_{page_number}_image_{image_number}"
            f"{image_extension}"
        )

        image_path = output_dir / image_filename

        image_path.write_bytes(image.data)

        total_images += 1

        print("Saved:", image_path)


print("\n--------------------")
print("Total extracted images:", total_images)
print("Output directory:", output_dir.resolve())
