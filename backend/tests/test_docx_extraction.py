
from pathlib import Path

from app.services.docx_extractor import extract_docx_content


docx_path = input("Enter DOCX file path: ").strip().strip('"')

output_dir = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "extracted_docx_images"
    / Path(docx_path).stem
)

print("\nDOCX EXTRACTION TEST")
print("--------------------")

try:

    result = extract_docx_content(
        file_path=docx_path,
        output_dir=output_dir
    )

    print("\nEXTRACTION RESULTS")
    print("------------------")

    print("Text blocks:", result["total_text_blocks"])
    print("Extracted images:", result["total_images"])
    print("Skipped images:", result["skipped_images"])

    print("\nEXTRACTED TEXT")

    for index, block in enumerate(result["text"], start=1):

        print(f"\nBlock {index} ({block['type']}):")
        print(block["content"][:300])

    print("\nEXTRACTED IMAGE DETAILS")

    for image in result["images"]:

        print(
            "Image:", image["image_number"],
            "| Dimensions:", image["width"], "x", image["height"],
            "| Format:", image["format"],
            "| Path:", image["image_path"]
        )

    print("\nDOCX extraction completed.")

except Exception as error:

    print("\nERROR:")
    print(error)
