
import base64
from pathlib import Path

from app.core.groq_client import client


def understand_image(image_path):

    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError("Image file was not found.")

    extension = image_path.suffix.lower()

    if extension == ".png":
        mime_type = "image/png"

    elif extension in [".jpg", ".jpeg"]:
        mime_type = "image/jpeg"

    else:
        raise ValueError("Only PNG and JPEG images are supported.")

    with open(image_path, "rb") as image_file:

        image_data = base64.b64encode(
            image_file.read()
        ).decode("utf-8")

    image_url = (f"data:{mime_type};base64,{image_data}")

    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """
                        Analyze this image.

                        1. Extract readable text.
                        2. Describe diagrams, charts, and figures.
                        3. Explain the main information.
                        4. Preserve important labels.
                        5. Do not guess unclear information.

                        Keep your response concise.
                        """
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    }
                ]
            }
        ],
        temperature=0.2,
        max_completion_tokens=700
    )

    return response.choices[0].message.content
