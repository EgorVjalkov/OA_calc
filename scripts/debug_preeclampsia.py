import fitz
import re

pdf_path = 'preeclampsia_test.pdf'
doc = fitz.open(pdf_path)

# Let's use the exact regex from our parser
uur_pattern = re.compile(
    r"Уровень\s+убедительности\s+рекомендаци[йи]\s+([AАBВ])\s*"
    r"\(?уровень\s+достоверности\s+доказательств\s*[-–—]?\s*(\d)\)?",
    re.IGNORECASE | re.MULTILINE | re.DOTALL
)

print("Starting to search for matches in text blocks...")
for page_num in range(doc.page_count):
    page = doc[page_num]
    blocks = page.get_text("blocks")
    text_blocks = [b for b in blocks if b[6] == 0]
    text_blocks.sort(key=lambda b: (b[1], b[0]))
    
    for b in text_blocks:
        text = b[4].strip()
        if "Уровень" in text and "убедительности" in text:
            match = uur_pattern.search(text)
            print("---")
            print(f"RAW TEXT (Page {page_num+1}):\n{repr(text)}")
            if match:
                print(f"MATCH: {match.group(1)} {match.group(2)}")
            else:
                print("NO MATCH! 🤔")
            
            # Print just a few to analyze
            if page_num > 18:
                break
    if page_num > 18:
        break
