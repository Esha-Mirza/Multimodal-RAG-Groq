
import base64
from pathlib import Path

from app.core.groq_client import client


image_path = Path(
    "data/extracted_images/page_4_image_1.jpg"
)

if not image_path.exists():
    print("Image file not found.")
    exit()


image_extension = image_path.suffix.lower()

if image_extension == ".png":
    mime_type = "image/png"
else:
    mime_type = "image/jpeg"


with open(image_path, "rb") as image_file:
    image_data = base64.b64encode(
        image_file.read()
    ).decode("utf-8")


image_url = (
    f"data:{mime_type};base64,{image_data}"
)


response = client.chat.completions.create(
    model="qwen/qwen3.8-27b",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": """
                    Analyze this image carefully.

                    1. Extract all readable text.
                    2. Describe diagrams, charts, and figures.
                    3. Explain the main information conveyed.
                    4. Preserve important labels and terminology.
                    5. Do not invent information if something
                       is unclear or unreadable.

                    Organize your response into clear sections.
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


print("\nIMAGE UNDERSTANDING RESULTS")
print("---------------------------")

print(response.choices[0].message.content)
