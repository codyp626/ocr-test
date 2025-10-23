import pytesseract
from PIL import Image

def ocr_image(image_path):
    """
    Perform OCR on the given image and return the extracted text.

    :param image_path: Path to the image file.
    :return: Extracted text from the image.
    """
    try:
        # Open the image file
        img = Image.open(image_path)


        # Use pytesseract to do OCR on the image
        text = pytesseract.image_to_string(img)

        return text
    except Exception as e:
        return f"An error occurred: {e}"
    
print(ocr_image('image2.png'))