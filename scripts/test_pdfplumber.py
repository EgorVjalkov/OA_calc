import pdfplumber
import json

def main():
    pdf_path = '/home/egr/OA_calc/test_1wY4larPpgCJINGcC3iT81Ovkj9VtnuV4.pdf'
    criteria_list = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if not table or not table[0]:
                    continue
                
                header = [str(c).lower().replace('\n', ' ') for c in table[0] if c]
                header_str = " ".join(header)
                
                # Check if this table looks like the Criteria table
                if 'критерии' in header_str and 'качества' in header_str:
                    for row in table[1:]:
                        if row and len(row) >= 2:
                            # Typically col 0 is N, col 1 is the Criteria text
                            # Sometimes N and Criteria are merged into col 0 if parsing is weird.
                            # Let's just collect the row representations for inspection
                            criteria_list.append(row)

    print(json.dumps(criteria_list[:5], ensure_ascii=False, indent=2))
    print(f"Total Criteria matched in this file: {len(criteria_list)}")

if __name__ == '__main__':
    main()
