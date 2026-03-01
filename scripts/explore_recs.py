import sys
import fitz
import re
import gdown
from pathlib import Path

def test_extract(file_id="1wY4larPpgCJINGcC3iT81Ovkj9VtnuV4", dest="test_recs.pdf"):
    print(f"Downloading PDF {file_id}...")
    gdown.download(f'https://drive.google.com/uc?id={file_id}', dest, quiet=True)
    
    if not Path(dest).exists():
        print("Download failed!")
        return

    print("Parsing PDF for strong recommendations (A/B)...")
    doc = fitz.open(dest)
    
    # Pattern to find Level A or B (handles cyrillic А, В and latin A, B)
    uur_pattern = re.compile(
        r"Уровень\s+убедительности\s+рекомендаций\s+([AАBВ])\s*"
        r"\(?уровень\s+достоверности\s+доказательств\s*[-–]\s*(\d)\)?",
        re.IGNORECASE | re.MULTILINE | re.DOTALL
    )

    recs = []
    
    for page_num in range(doc.page_count):
        page = doc[page_num]
        # get_text("blocks") returns (x0, y0, x1, y1, text, block_no, block_type)
        blocks = page.get_text("blocks")
        
        # We need block_type == 0 (text)
        text_blocks = [b for b in blocks if b[6] == 0]
        # Sort top-to-bottom
        text_blocks.sort(key=lambda b: (b[1], b[0]))
        
        for i, b in enumerate(text_blocks):
            text = b[4].strip()
            match = uur_pattern.search(text)
            if match:
                level = match.group(1).upper()
                if level == 'А': level = 'A'
                if level == 'В': level = 'B'
                evidence = match.group(2)
                
                # Check previous block for recommendation text
                rec_text = ""
                if i > 0:
                    rec_text = text_blocks[i-1][4].strip()
                    rec_text = " ".join(rec_text.split()) # clean newlines
                    
                recs.append({
                    "page": page_num + 1,
                    "level": level,
                    "evidence": evidence,
                    "text": rec_text
                })

    for i, r in enumerate(recs):
        print(f"\n--- Rec {i+1} ---")
        print(f"Level: {r['level']} (Evidence {r['evidence']}) | Page: {r['page']}")
        if r['text'].startswith("Комментари"):
            print("WARNING: Extracted Comment instead of Recommendation!")
        print(f"Text: {r['text'][:200]}...")
        
    print(f"\nTotal A/B recommendations found: {len(recs)}")

if __name__ == "__main__":
    test_extract()
