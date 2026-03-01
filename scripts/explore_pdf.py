import requests
from bs4 import BeautifulSoup
import re
import fitz  # PyMuPDF
import gdown
import os

def download_pdf(file_id, dest):
    """Downloads a file from Google Drive using gdown."""
    url = f'https://drive.google.com/uc?id={file_id}'
    gdown.download(url, dest, quiet=False)

def main():
    print("Fetching Roag Portal...")
    res = requests.get("https://roag-portal.ru/recommendations_obstetrics")
    soup = BeautifulSoup(res.text, 'html.parser')
    
    links = soup.find_all('a', href=re.compile(r'drive\.google\.com/file/d/'))
    if not links:
        print("No links found!")
        return
    
    # Grab the first link for exploratory testing
    first_link = links[0]
    name = first_link.text.strip()
    href = first_link['href']
    match = re.search(r'/d/([^/]+)/', href)
    if not match:
        print("No file id found")
        return
    file_id = match.group(1)
    
    print(f"Pathology: {name}")
    print(f"File ID: {file_id}")
    
    pdf_path = f"test_{file_id}.pdf"
    if not os.path.exists(pdf_path):
        print("Downloading PDF...")
        download_pdf(file_id, pdf_path)
    else:
        print(f"File {pdf_path} already exists. Skipping download.")
    
    print("Parsing PDF...")
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text("text") + "\n"
    
    # Simple search heuristics
    search_strs = ["Критерии качества оказания", "КРИТЕРИИ КАЧЕСТВА"]
    
    idx = -1
    for s in search_strs:
        idx = full_text.find(s)
        if idx != -1:
            print(f"FOUND HEADER: '{s}'")
            break
            
    if idx != -1:
        snippet = full_text[idx:idx+5000]
        print("--- SNIPPET ---")
        # Print a small portion to console
        print(snippet[:1500])
        print("---------------")
        with open("criteria_snippet.txt", "w", encoding="utf-8") as f:
            f.write(snippet)
        print("Saved snippet to criteria_snippet.txt")
    else:
        print("Header not found. Try case insensitive or different parsing.")

if __name__ == "__main__":
    main()
