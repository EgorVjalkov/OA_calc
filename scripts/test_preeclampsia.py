import json
from parse_recommendations import process_pdf

recs = process_pdf('preeclampsia_test.pdf')
print(json.dumps(recs, ensure_ascii=False, indent=2))
print(f"Total strong recommendations found: {len(recs)}")
