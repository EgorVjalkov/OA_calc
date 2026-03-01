import os
import json
import re
import requests
from bs4 import BeautifulSoup
import gdown
import pdfplumber
import tempfile
from pathlib import Path

DATA_DIR = Path("/home/egr/OA_calc/oac/program_logic/data")
URL = "https://roag-portal.ru/recommendations_obstetrics"

def download_pdf(file_id, dest):
    """Downloads a file from Google Drive."""
    url = f'https://drive.google.com/uc?id={file_id}'
    gdown.download(url, dest, quiet=True)

def clean_text(text):
    if not text:
        return ""
    # Replace newlines with spaces
    text = text.replace('\n', ' ')
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    # Remove weird artifact numbers at the end (sometimes tables have footnote markers)
    # This is a bit risky if a number is part of the sentence, so we just strip trailing spaces
    return text.strip()

def process_pdf(pdf_path):
    criteria = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if not table or not table[0]:
                    continue
                
                header = [str(c).lower().replace('\n', ' ') for c in table[0] if c]
                header_str = " ".join(header)
                
                # Identify criteria table
                if 'критерии' in header_str and 'качества' in header_str:
                    for row in table[1:]:
                        if len(row) >= 2:
                            # Depending on the table structure, column indices could vary
                            # Typically: 0 -> №, 1 -> Criteria Text, 2 -> Evaluation
                            # But sometimes 0 -> combined or 1 -> Criteria Text
                            text_col = 1 if len(row) > 1 else 0
                            
                            # A heuristic: the criteria text is usually the longest string in the row
                            longest_str = max([str(cell) if cell else "" for cell in row], key=len)
                            
                            cleaned = clean_text(longest_str)
                            if len(cleaned) > 10 and not cleaned.lower().startswith('критерии качества'):
                                criteria.append(f"• {cleaned}")
                                
    return "\n".join(criteria)

def main():
    print("Fetching Roag Portal...")
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    links = soup.find_all('a', href=re.compile(r'drive\.google\.com/file/d/'))
    if not links:
        print("No links found!")
        return
        
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    results = {}
    
    with tempfile.TemporaryDirectory() as tmpdir:
        for i, link in enumerate(links):
            name = clean_text(link.text)
            href = link['href']
            
            match = re.search(r'/d/([^/]+)/', href)
            if not match:
                continue
            
            file_id = match.group(1)
            print(f"[{i+1}/{len(links)}] Downloading: {name} (ID: {file_id})")
            
            pdf_path = os.path.join(tmpdir, f"{file_id}.pdf")
            try:
                download_pdf(file_id, pdf_path)
                criteria_text = process_pdf(pdf_path)
                
                if criteria_text:
                    results[name] = criteria_text
                    print(f"  -> Extracted {len(criteria_text.splitlines())} criteria.")
                else:
                    print(f"  -> Warning: No criteria found for {name}.")
                    
            except Exception as e:
                print(f"  -> Error processing {name}: {e}")
                
    output_path = DATA_DIR / "criteria.json"
    print(f"Saving {len(results)} pathologies to {output_path}")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
        
    print("Done!")

if __name__ == "__main__":
    main()
