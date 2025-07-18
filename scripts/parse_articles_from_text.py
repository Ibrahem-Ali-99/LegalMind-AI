import re
import csv
import os

from pathlib import Path


script_dir = Path(__file__).parent


project_root = script_dir.parent

INPUT_FILE = project_root / "data" / "txt" / "raw_ocr_output_constitution.txt"
OUTPUT_FILE = project_root / "data" / "csv" / "egyptian_constitution.csv"
CSV_HEADERS = ['Arabic Number', 'English Number', 'Arabic Article', 'Article Number (EN)', 'Text']


def to_arabic_indic(number):
    to_ar_indic_map = str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩')
    return str(number).translate(to_ar_indic_map)

def main():

    if not os.path.exists(INPUT_FILE):
        print(f"Error: Input file '{INPUT_FILE}' not found.")
        print("Please make sure the OCR file is in the same directory as this script.")
        return

    print(f"Reading data from '{INPUT_FILE}'...")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        full_text = f.read()

    article_pattern = r'(ماد[ةه]\s*\((?:.+?)\))'
    
    
    chunks = re.split(article_pattern, full_text)
    
    article_texts = [chunks[i+1] for i in range(1, len(chunks), 2)]
    
    csv_rows = []

   
    for index, text_content in enumerate(article_texts):
        
        article_num = index + 1

        if "الفهرس" in text_content:
            text_content = text_content.split("الفهرس")[0]
        text_content = re.sub(r'\s+', ' ', text_content).strip()


        ar_indic_num_str = to_arabic_indic(article_num)
        
        en_num_str = str(article_num)
        
        arabic_article_header = f"مادة ({ar_indic_num_str})"
        
        en_article_num_str = str(article_num)

        csv_rows.append([
            ar_indic_num_str,
            en_num_str,
            arabic_article_header,
            en_article_num_str,
            text_content
        ])

    print(f"Writing generated sequential data to '{OUTPUT_FILE}'...")
    try:
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADERS)
            writer.writerows(csv_rows)
        print("Successfully created the CSV file with a clean, generated index.")
    except IOError:
        print(f"Error: Could not write to file '{OUTPUT_FILE}'. Please check permissions.")

if __name__ == '__main__':
    main()