import json
import os

def main():
    json_path = '/home/egr/OA_calc/oac/program_logic/data/criteria.json'
    if not os.path.exists(json_path):
        print(f"File not found: {json_path}")
        return
        
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    print(f"Всего загружено патологий: {len(data)}\n")
    for path_name, criteria in data.items():
        print("=" * 80)
        print(f"ПАТОЛОГИЯ: {path_name}")
        print("-" * 80)
        print(criteria)
        print("=" * 80)
        print("\n")

if __name__ == '__main__':
    main()
