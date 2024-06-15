import pandas as pd
from dataclasses import dataclass, fields, InitVar
from typing import Optional
from fastnumbers import fast_real

from oac.program_logic.patientparameter import Limits
from oac.program_logic.my_table import get_my_table_string


translation_dict = {
    'oxygenation': 'оксигенация',
    'plt': 'коагуляция',
    'bili': 'печень',
    'hypotension_count': 'гемодинамика',
    'glasgow': 'ЦНС',
    'excretion': 'почки'
}


@dataclass
class BaseScale:
    pass

    def __post_init__(self):
        self.data: Optional[pd.DataFrame] = None
        self.lethality_frame: Optional[pd.DataFrame] = None
        self.total_score = 0

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

    def get_score(self, indicator_name: str) -> int:
        score_scale = self.get_score_scale(indicator_name)
        for score in score_scale.index:
            cell_data = score_scale[score]
            limits = Limits(
                *[fast_real(e) for e in cell_data.split()])
            if self.__dict__[indicator_name].value in limits:
                return score

# здесь узкое место. не очевидно как размутиться
    def get_simple_scores(self):
        field_names = [i.name for i in fields(self)]
        scores = {}
        for indicator_name in field_names:
            scores[indicator_name] = self.get_score(indicator_name)

        return scores

    def get_lethality(self):
        return self.get_score('total_score')

