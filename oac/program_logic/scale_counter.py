import pandas as pd
from dataclasses import dataclass, fields
from typing import Optional, Callable
from fastnumbers import fast_real, fast_int
from collections import namedtuple

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
        self.data: Optional[pd.DataFrame] = None
        self.lethality_frame: Optional[pd.DataFrame] = None
        self.total_score: Optional[ShortParam] = None

    def get_scale_frame(self, scale_name: str):
        path = 'program_logic/data/scales.xlsx'
        self.data = pd.read_excel(path, sheet_name=scale_name+'_count', index_col=0, dtype=str)
        self.lethality_frame = pd.read_excel(path, sheet_name=scale_name+'_lethal', index_col=0)

    def get_score_scale(self, indicator_name: str) -> pd.Series:
        if indicator_name == 'total_score':
            indicator_ser = self.lethality_frame.loc[indicator_name]
        else:
            indicator_ser = self.data.loc[indicator_name]

        indicator_ser = indicator_ser[indicator_ser.map(pd.notna) == True]
        return indicator_ser

    def get_score(self, indicator_name: str) -> ScaleParam:
        param: ShortParam = self.__dict__[indicator_name]
        score_scale = self.get_score_scale(indicator_name)

        for score in score_scale.index:
            cell_data = score_scale[score]
            limits = Limits(
                *[fast_real(e) for e in cell_data.split()])
            if param.value in limits:
                return ScaleParam(param.name, param.value, score)

    def get_simple_scores(self):
        field_names = [i.name for i in fields(self)]
        scores = {}
        for indicator_name in field_names:
            scores[indicator_name] = self.get_score(indicator_name)

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
