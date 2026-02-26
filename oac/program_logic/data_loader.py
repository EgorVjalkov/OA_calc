import json
from pathlib import Path

class DataLoader:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataLoader, cls).__new__(cls)
            cls._instance._load_data()
        return cls._instance

    def _load_data(self):
        data_dir = Path(__file__).parent / 'data'
        
        # Load parameters
        with open(data_dir / 'parameters.json', 'r', encoding='utf-8') as f:
            self.parameters_data = json.load(f)
            
        # Load scales
        with open(data_dir / 'scales.json', 'r', encoding='utf-8') as f:
            self.scales_data = json.load(f)
            
        # Load drug dosage
        with open(data_dir / 'drug_dosage.json', 'r', encoding='utf-8') as f:
            self.drug_dosage_data = json.load(f)

# Global singleton instance
data_loader = DataLoader()
