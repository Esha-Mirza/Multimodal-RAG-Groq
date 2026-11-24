
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
    content_blocks = []

    skipped_images = 0
    image_number = 0

    image_relationships = {}

    for relationship in document.part.rels.values():

        if "image" in relationship.reltype:
            image_relationships[relationship.rId] = relationship.target_part

    def extract_image(relationship_id):

        nonlocal image_number, skipped_images

        if relationship_id not in image_relationships:
            return None

        image_number += 1

        image_data = image_relationships[relationship_id].blob

        try:

            with Image.open(BytesIO(image_data)) as img:

                width, height = img.size
                image_format = img.format

                if width < MIN_IMAGE_WIDTH or height < MIN_IMAGE_HEIGHT:
                    skipped_images += 1
                    return None

                if image_format not in ["PNG", "JPEG"]:
                    skipped_images += 1
                    return None

                extension = ".png" if image_format == "PNG" else ".jpg"

                image_filename = f"image_{image_number}{extension}"

                output_dir.mkdir(
                    parents=True,
                    exist_ok=True
                )

                image_path = output_dir / image_filename

                img.verify()

            image_path.write_bytes(image_data)

            image_info = {
                "image_number": image_number,
                "image_path": str(image_path),
                "width": width,
                "height": height,
                "format": image_format
            }

            extracted_images.append(image_info)

            return image_info

        except Exception:
            skipped_images += 1
            return None

    def extract_paragraph_images(paragraph_element):

        image_blocks = []

        for element in paragraph_element.iter():

            if element.tag.endswith("}blip"):

                relationship_id = element.get(
                    "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"
                )

                if relationship_id:

                    image_info = extract_image(relationship_id)

                    if image_info:
                        image_blocks.append({
                            "type": "image",
                            **image_info
                        })

        return image_blocks

    for element in document.element.body:

        if element.tag.endswith("}p"):

            for paragraph in document.paragraphs:

                if paragraph._element is element:

                    text = paragraph.text.strip()

                    if text:

                        text_block = {
                            "type": "text",
                            "content": text,
                            "style": paragraph.style.name
                        }

                        extracted_text.append(text_block)
                        content_blocks.append(text_block)

                    content_blocks.extend(
                        extract_paragraph_images(element)
                    )

                    break

        elif element.tag.endswith("}tbl"):

            for table in document.tables:

                if table._element is element:

                    table_rows = []

                    for row in table.rows:

                        row_text = [
                            cell.text.strip()
                            for cell in row.cells
                        ]

                        row_text = [
                            text for text in row_text if text
                        ]

                        if row_text:
                            table_rows.append(" | ".join(row_text))

                    if table_rows:

                        table_block = {
                            "type": "table",
                            "content": "\n".join(table_rows)
                        }

                        extracted_text.append(table_block)
                        content_blocks.append(table_block)

                    break

    return {
        "text": extracted_text,
        "images": extracted_images,
        "content_blocks": content_blocks,
        "total_text_blocks": len(extracted_text),
        "total_images": len(extracted_images),
        "skipped_images": skipped_images
    }
