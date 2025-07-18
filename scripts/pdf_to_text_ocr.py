import os
from pathlib import Path
from pdf2image import convert_from_path
import pytesseract
from dotenv import load_dotenv

load_dotenv()

TESSERACT_PATH = os.getenv("TESSERACT_EXECUTABLE_PATH")
POPPLER_PATH = os.getenv("POPPLER_BIN_PATH")

PROJECT_ROOT = Path(__file__).parent.parent

SOURCE_PDF_DIR = PROJECT_ROOT / "data" / "0_source_pdfs"
OUTPUT_TXT_DIR = PROJECT_ROOT / "data" / "1_raw_text"

PDF_FILENAME = "دستور-جمهورية-مصر-العربية-2019.pdf"
OUTPUT_FILENAME = "raw_ocr_output_constitution.txt"

PDF_PATH = SOURCE_PDF_DIR / PDF_FILENAME
OUTPUT_PATH = OUTPUT_TXT_DIR / OUTPUT_FILENAME

TESSERACT_CONFIG = r'--oem 3 --psm 6 -l ara'


def convert_pdf_to_images(pdf_path, dpi=300, poppler_path=None):
    print("Converting PDF to images...")
    return convert_from_path(pdf_path, dpi=dpi, poppler_path=poppler_path)


def extract_text_from_images(pages, config):
    print("Extracting text using Tesseract OCR...")
    full_text = []
    for i, page in enumerate(pages):
        text = pytesseract.image_to_string(page, config=config)
        full_text.append(f"\n\n===== Page {i+1} =====\n{text}")
        print(f"Page {i+1} processed.")
    return "".join(full_text)


def save_text_to_file(text, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(text)
    print(f"\n Done. OCR text saved to: {output_path}")


def main():
    pages = convert_pdf_to_images(PDF_PATH, poppler_path=POPLER_BIN_PATH)
    extracted_text = extract_text_from_images(pages, config=TESSERACT_CONFIG)
    save_text_to_file(extracted_text, OUTPUT_PATH)


if __name__ == "__main__":
    main()
