
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

    print("\nEXTRACTION SUMMARY")
    print("------------------")

    print("Text blocks:", result["total_text_blocks"])
    print("Extracted images:", result["total_images"])
    print("Skipped images:", result["skipped_images"])
    print("Total content blocks:", len(result["content_blocks"]))

    print("\nDOCUMENT CONTENT IN ORDER")
    print("-------------------------")

    for index, block in enumerate(result["content_blocks"], start=1):

        print(f"\nBlock {index} ({block['type']}):")

        if block["type"] == "image":

            print("Image number:", block["image_number"])
            print("Dimensions:", block["width"], "x", block["height"])
            print("Format:", block["format"])
            print("Path:", block["image_path"])

        else:
            print(block["content"][:300])

    print("\nDOCX extraction completed.")

except Exception as error:

    print("\nERROR:")
    print(error)
