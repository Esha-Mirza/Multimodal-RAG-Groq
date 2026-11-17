
from app.services.image_understanding_service import understand_image


image_path = "data/extracted_images/page_4_image_1.jpg"


print("\nIMAGE UNDERSTANDING SERVICE TEST")
print("--------------------------------")

try:

    result = understand_image(image_path)

    print("\nRESULT:")
    print(result)

except Exception as error:

    print("\nERROR:")
    print(error)
