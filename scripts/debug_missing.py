import pdfplumber
import pprint
import gdown
import os

def main():
    file_id = '1VsGbb6LQ1kfiG4wHYwoAbK56z0L8Ik9s'
    pdf_path = f'/home/egr/OA_calc/test_{file_id}.pdf'
    if not os.path.exists(pdf_path):
        gdown.download(f'https://drive.google.com/uc?id={file_id}', pdf_path, quiet=True)
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            for t_idx, table in enumerate(tables):
                if not table or not table[0]: continue
                
                header = [str(c).lower().replace('\n', ' ') for c in table[0] if c]
                header_str = " ".join(header)
                
                # Check if it has any relation to criteria
                if 'критери' in header_str or 'качества' in header_str:
                    print(f"Page {page_num+1}, Table {t_idx+1}:")
                    print("HEADER STR:", header_str)
                    print("RAW HEADER:", table[0])
                    print("FIRST ROW:", table[1] if len(table)>1 else "No row")
                    print("-" * 40)
                    
                # also print if the text itself says 'Критерии качества'
                text = page.extract_text() or ""
                if 'Критерии качества' in text:
                    # just to know which pages it appears on
                    if 'критери' not in header_str:
                        print(f"Text 'Критерии качества' found on page {page_num+1} but not matched as table header")

if __name__ == '__main__':
    main()
