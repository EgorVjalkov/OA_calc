import json
from dataclasses import dataclass, fields
from typing import Optional, Callable
from fastnumbers import fast_real, fast_int
from collections import namedtuple
from pathlib import Path

from oac.program_logic.patientparameter import Limits
from oac.program_logic.parameters import ShortParam
from oac.program_logic.my_table import get_my_table_string


translation_dict = {
    'oxygenation': 'оксигенация',
    'plt': 'коагуляция',
    'bili': 'печень',
    'hypotension_count': 'гемодинамика',
    'glasgow': 'ЦНС',
    'excretion': 'почки'
}

ScaleParam = namedtuple('ScaleParam', 'name value score')


@dataclass
class BaseScale:
    pass

    def __post_init__(self):
        self.data: Optional[dict] = None
        self.lethality_frame: Optional[dict] = None
        self.total_score: Optional[ShortParam] = None

    def get_scale_frame(self, scale_name: str):
        path = Path(__file__).parent / 'data' / 'scales.json'
        with open(path, 'r', encoding='utf-8') as f:
            full_data = json.load(f)
            
        self.data = full_data[f"{scale_name}_count"]
        self.lethality_frame = full_data[f"{scale_name}_lethal"]

    def get_score_scale(self, indicator_name: str) -> dict:
        if indicator_name == 'total_score':
            indicator_dict = self.lethality_frame.get(indicator_name, {})
        else:
            indicator_dict = self.data.get(indicator_name, {})

        # Filter out null values to replicate pandas dropna
        return {k: v for k, v in indicator_dict.items() if v is not None}

    def get_score(self, indicator_name: str) -> ScaleParam:
        param: ShortParam = self.__dict__[indicator_name]
        score_scale = self.get_score_scale(indicator_name)

        for score, cell_data in score_scale.items():
            cell_data = str(cell_data)
            if '*' in cell_data:
                if str(param.value) == cell_data.replace('*', ''):
                    return ScaleParam(param.name, param.value, score)

            else:
                limits = Limits(
                    *[fast_real(e) for e in cell_data.split()])
                if param.value in limits:
                    return ScaleParam(param.name, param.value, score)

    def get_simple_scores(self):
        field_names = [i.name for i in fields(self)]
        scores = {}
        for indicator_name in field_names:
            score = self.get_score(indicator_name)
            if score is None:
                print(f"DEBUG: get_score returned None for {indicator_name} with value {self.__dict__[indicator_name]}")
            scores[indicator_name] = score

        return scores

    def get_total_score(self, scores) -> int:
        scores = [fast_int(i.score) for i in scores.values()]
        self.total_score = ShortParam('total_score', sum(scores))
        return self.total_score

    def get_lethality(self):
        return self.get_score('total_score')

    def __call__(self, get_scores: Callable, *args, **kwargs):
        scores: dict = get_scores()
        self.get_total_score(scores)
        lethal = self.get_lethality()
        rows = [[i.name, i.value, i.score] for i in scores.values()]
        rows.append(['сумма', '', lethal.value])
        rows.append(['летальность', '', lethal.score])

        my_table = get_my_table_string(header=False, rows=rows)
        return my_table
