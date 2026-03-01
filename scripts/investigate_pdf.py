import os
import fitz
import gdown

file_id = '1_XxcivLg5KpPTrNNBtExJYa83Yg29suj'
pdf_path = 'preeclampsia_test.pdf'

import requests

if not os.path.exists(pdf_path):
    print("Downloading PDF...")
    url = f'https://drive.google.com/uc?id={file_id}&export=download'
    res = requests.get(url)
    with open(pdf_path, 'wb') as f:
        f.write(res.content)

print("Opening PDF...")
doc = fitz.open(pdf_path)

print("Searching for 'Уровень'...")
for page_num in range(doc.page_count):
    page = doc[page_num]
    blocks = page.get_text("blocks")
    text_blocks = [b for b in blocks if b[6] == 0]
    text_blocks.sort(key=lambda b: (b[1], b[0]))
    
    for b in text_blocks:
        text = b[4].strip()
        if "уров" in text.lower() and "рекомендац" in text.lower():
            print(f"--- PAGE {page_num + 1} ---")
            print(text)
            print("-----------------------")
