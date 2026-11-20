
from pathlib import Path
from io import BytesIO

from docx import Document
from PIL import Image


MIN_IMAGE_WIDTH = 100
MIN_IMAGE_HEIGHT = 100


def extract_docx_content(file_path, output_dir):

    file_path = Path(file_path)
    output_dir = Path(output_dir)

    if not file_path.exists():
        raise FileNotFoundError("DOCX file was not found.")

    if file_path.suffix.lower() != ".docx":
        raise ValueError("Only DOCX files are supported.")

    document = Document(str(file_path))

    extracted_text = []
    extracted_images = []
    skipped_images = 0

    image_number = 0

    for element in document.element.body:

        # Extract paragraphs
        if element.tag.endswith("}p"):

            for paragraph in document.paragraphs:

                if paragraph._element is element:

                    text = paragraph.text.strip()

                    if text:
                        extracted_text.append({
                            "type": "text",
                            "content": text,
                            "style": paragraph.style.name
                        })

                    break

        # Extract tables
        elif element.tag.endswith("}tbl"):

            for table in document.tables:

                if table._element is element:

                    for row in table.rows:

                        row_text = [
                            cell.text.strip()
                            for cell in row.cells
                        ]

                        row_text = [
                            text for text in row_text if text
                        ]

                        if row_text:
                            extracted_text.append({
                                "type": "table",
                                "content": " | ".join(row_text)
                            })

                    break

    # Extract embedded images
    for relationship in document.part.rels.values():

        if "image" not in relationship.reltype:
            continue

        image_number += 1

        image_data = relationship.target_part.blob

        try:

            with Image.open(BytesIO(image_data)) as img:

                width, height = img.size
                image_format = img.format

                if width < MIN_IMAGE_WIDTH or height < MIN_IMAGE_HEIGHT:
                    skipped_images += 1
                    continue

                if image_format not in ["PNG", "JPEG"]:
                    skipped_images += 1
                    continue

                extension = ".png" if image_format == "PNG" else ".jpg"

                image_filename = f"image_{image_number}{extension}"

                output_dir.mkdir(
                    parents=True,
                    exist_ok=True
                )

                image_path = output_dir / image_filename

                img.verify()

            image_path.write_bytes(image_data)

            extracted_images.append({
                "image_number": image_number,
                "image_path": str(image_path),
                "width": width,
                "height": height,
                "format": image_format
            })

        except Exception:
            skipped_images += 1

    return {
        "text": extracted_text,
        "images": extracted_images,
        "total_text_blocks": len(extracted_text),
        "total_images": len(extracted_images),
        "skipped_images": skipped_images
    }
