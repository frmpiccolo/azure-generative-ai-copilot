from PIL import Image
import pytesseract

def extract_text_from_image_file(file) -> str:
    image = Image.open(file)
    return pytesseract.image_to_string(image)
