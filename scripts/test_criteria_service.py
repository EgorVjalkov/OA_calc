import sys
import os

# Add project root to path so we can import 'oac' module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from oac.program_logic.criteria_service import CriteriaService

def test():
    print("Testing CriteriaService...")
    service = CriteriaService()
    pathologies = service.get_all_pathologies()
    print(f"Total pathologies loaded: {len(pathologies)}")
    if pathologies:
        print(f"First pathology: {pathologies[0]}")
        text = service.get_criteria(pathologies[0])
        print("Data sample:")
        print("-" * 40)
        print(text)
        print("-" * 40)

if __name__ == "__main__":
    test()
