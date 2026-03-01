import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class CriteriaService:
    def __init__(self, data_path: str = "oac/program_logic/data"):
        """
        Инициализирует сервис Критериев качества и Рекомендаций, загружает JSON в память.
        """
        self.data_dir = Path(data_path)
        self.criteria_data: Dict[str, str] = {}
        self.recommendations_data: Dict[str, List[Dict[str, str]]] = {}
        self._load_data()

    def _load_data(self):
        criteria_path = self.data_dir / "criteria.json"
        recs_path = self.data_dir / "recommendations.json"
        
        # Load Criteria
        try:
            if criteria_path.exists():
                with open(criteria_path, "r", encoding="utf-8") as f:
                    self.criteria_data = json.load(f)
                logger.info(f"Loaded criteria for {len(self.criteria_data)} pathologies.")
            else:
                logger.warning(f"Criteria file not found at {criteria_path}")
        except Exception as e:
            logger.error(f"Error loading criteria data: {e}")
            
        # Load Recommendations
        try:
            if recs_path.exists():
                with open(recs_path, "r", encoding="utf-8") as f:
                    self.recommendations_data = json.load(f)
                logger.info(f"Loaded recommendations for {len(self.recommendations_data)} pathologies.")
            else:
                logger.warning(f"Recommendations file not found at {recs_path}")
        except Exception as e:
            logger.error(f"Error loading recommendations data: {e}")

    def get_all_criteria_pathologies(self) -> List[str]:
        """Возвращает отсортированный список патологий, для которых есть критерии качества."""
        return sorted(self.criteria_data.keys())

    def get_all_recommendation_pathologies(self) -> List[str]:
        """Возвращает отсортированный список патологий, для которых есть клинические рекомендации."""
        return sorted(self.recommendations_data.keys())

    def get_criteria(self, pathology_name: str) -> Optional[str]:
        """Возвращает текст критериев по названию патологии."""
        return self.criteria_data.get(pathology_name)

    def get_recommendations(self, pathology_name: str) -> List[Dict[str, str]]:
        """Возвращает список рекомендаций для патологии. Каждая рекомендация - это словарь с ключами short_level, text, page."""
        return self.recommendations_data.get(pathology_name, [])

# Singleton
criteria_service = CriteriaService()
