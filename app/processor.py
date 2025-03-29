import os
from app.api import ask_openai
from app.ocr import extract_text_from_image_file

TEXT_EXT = [".txt"]
IMG_EXT = [".png", ".jpg", ".jpeg"]

def read_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def save_response(filename: str, content: str):
    os.makedirs("outputs", exist_ok=True)
    path = os.path.join("outputs", filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def process_file(file_path: str):
    ext = os.path.splitext(file_path)[1].lower()
    if ext in TEXT_EXT:
        prompt = read_file(file_path)
    elif ext in IMG_EXT:
        prompt = extract_text_from_image_file(file_path)
    else:
        raise ValueError("Unsupported file format")
    
    result = ask_openai(prompt)
    output_file = os.path.basename(file_path).replace(ext, "_response.txt")
    save_response(output_file, result)
    return output_file, result
