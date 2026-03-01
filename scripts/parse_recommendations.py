import os
import json
import re
import requests
from bs4 import BeautifulSoup
import gdown
import fitz
import tempfile
from pathlib import Path

# Paths
DATA_DIR = Path("/home/egr/OA_calc/oac/program_logic/data")
URL = "https://roag-portal.ru/recommendations_obstetrics"

# Regex Patterns
# Matches: Уровень убедительности рекомендаций А (уровень достоверности доказательств - 1)
uur_pattern = re.compile(
    r"Уровень\s+убедительности\s+рекомендаци[йи]\s+([AАBВ])\s*"
    r"\(?уровень\s+достоверности\s+доказательств\s*[-–—]?\s*(\d)\)?",
    re.IGNORECASE | re.MULTILINE | re.DOTALL
)

# Removes exact UUR strings that might be inside the captured text
uur_exact_str_pattern = re.compile(
    r"Уровень\s+убедительности\s+рекомендаци[йи]\s+[AАBВCС]\s*"
    r"\(?уровень\s+достоверности\s+доказательств\s*[-–—]?\s*\d\)?\.?",
    re.IGNORECASE | re.MULTILINE | re.DOTALL
)

# Removes ATX links: (АТХ: B01AB группа гепарина)
atx_pattern = re.compile(r"\(АТХ:[^)]+\)", re.IGNORECASE)

# Removes literature references: [11-22], [42], [1, 2, 3]
lit_pattern = re.compile(r"\[[\d\s,.\-–]+\]")

# Strips leading bullets: •, -, —
bullet_pattern = re.compile(r"^[\s•\-\—]+")

def download_pdf(file_id, dest):
    """Downloads a file from Google Drive bypassing gdown quota."""
    url = f'https://drive.google.com/uc?id={file_id}&export=download'
    res = requests.get(url)
    with open(dest, 'wb') as f:
        f.write(res.content)

def clean_rec_text(text):
    if not text:
        return ""
    # Simplify whitespace
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)
    
    # Apply regex removals
    text = atx_pattern.sub('', text)
    text = lit_pattern.sub('', text)
    text = uur_exact_str_pattern.sub('', text)
    
    # Strip bullets and whitespace
    text = text.strip()
    text = bullet_pattern.sub('', text).strip()
    
    # Cleanup any double spaces left behind by removals
    text = re.sub(r'\s+', ' ', text)
    
    return text

def process_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    recs = []
    
    for page_num in range(doc.page_count):
        page = doc[page_num]
        blocks = page.get_text("blocks")
        
        # We only care about text blocks (type 0)
        text_blocks = [b for b in blocks if b[6] == 0]
        # Sort vertically inside a page
        text_blocks.sort(key=lambda b: (b[1], b[0]))
        
        # Join all blocks with spaces so regex can span across blocks
        full_page_text = " ".join([b[4].strip() for b in text_blocks])
        
        for match in uur_pattern.finditer(full_page_text):
            level = match.group(1).upper()
            if level == 'А': level = 'A'
            if level == 'В': level = 'B'
            evidence = match.group(2)
            short_level = f"{level}{evidence}" # e.g., A1, B2
            
            # Where is the recommendation text?
            match_start = match.start()
            
            # Look backwards up to 3000 characters for the preceding paragraph
            search_start = max(0, match_start - 3000)
            prior_text_chunk = full_page_text[search_start:match_start]
            
            # A good heuristic is to split by UUR matches and take the last part, 
            # so we don't grab the previous recommendation's text.
            parts = uur_pattern.split(prior_text_chunk)
            if parts:
                rec_text = parts[-1]
            else:
                rec_text = prior_text_chunk
                
            cleaned_text = clean_rec_text(rec_text)
            
            # Ignore if it accidentally grabbed a comment or is too short
            if len(cleaned_text) > 10 and not cleaned_text.lower().startswith('комментари'):
                recs.append({
                    "short_level": short_level,
                    "text": cleaned_text,
                    "page": page_num + 1,
                    "sort_key": f"{level}{evidence}" # works for 'A1' < 'A2' < 'B1'
                })
                    
    # Sort recommendations A1 -> A2 -> B1 -> B2 etc.
    recs.sort(key=lambda x: x["sort_key"])
    
    # Clean up sort_key before storing
    for r in recs:
        del r["sort_key"]
        
    return recs

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
            name = clean_rec_text(link.text)
            href = link['href']
            
            match = re.search(r'/d/([^/]+)/', href)
            if not match:
                continue
            
            file_id = match.group(1)
            print(f"[{i+1}/{len(links)}] Downloading: {name} (ID: {file_id})")
            
            pdf_path = os.path.join(tmpdir, f"{file_id}.pdf")
            try:
                download_pdf(file_id, pdf_path)
                recs = process_pdf(pdf_path)
                
                if recs:
                    results[name] = recs
                    print(f"  -> Extracted {len(recs)} A/B recommendations.")
                else:
                    print(f"  -> Warning: No strong recs found for {name}.")
                    
            except Exception as e:
                print(f"  -> Error processing {name}: {e}")
                
    output_path = DATA_DIR / "recommendations.json"
    print(f"Saving {len(results)} pathologies to {output_path}")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
        
    print("Done Phase 3 Parsing!")

if __name__ == "__main__":
    main()
