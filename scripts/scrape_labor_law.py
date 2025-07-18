import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

headers = {'User-Agent': 'Mozilla/5.0'}
url = 'https://manshurat.org/content/qnwn-lml-ljdyd-2025'

response = requests.get(url, headers=headers, timeout=30)
soup = BeautifulSoup(response.text, 'lxml')
paragraphs = soup.find_all('p')

articles = []
i = 0
while i < len(paragraphs):
    p_text = paragraphs[i].get_text(strip=True)
    if re.match(r'^مادة\s*\((.+?)\)', p_text):
        arabic_number = re.match(r'^مادة\s*\((.+?)\)', p_text).group(1).strip()
        english_number = str(int(arabic_number.translate(str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789'))))
        article_heading = p_text
        article_number_en = float(english_number)

        content = ''
        if i + 1 < len(paragraphs):
            next_text = paragraphs[i + 1].get_text(strip=True)
            if not re.match(r'^مادة\s*\(.+?\)', next_text):
                content = next_text
                i += 1

        articles.append({
            "Arabic Number": arabic_number,
            "English Number": english_number,
            "Arabic Article": article_heading,
            "Article Number (EN)": article_number_en,
            "Text": content
        })
    i += 1

df = pd.DataFrame(articles)
df.to_csv("egyptian_labor_law_2025.csv", index=False, encoding='utf-8-sig')
