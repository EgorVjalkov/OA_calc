import pandas as pd
from dataclasses import dataclass, fields, InitVar
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
class SofaCounter:
    fio2: InitVar[float | int]
    pao2: InitVar[int]
    resp_support_count: InitVar[str]
    plt: int
    bili: int
    hypotension_count: int
    glasgow: int
    crea: InitVar[int]
    diuresis: InitVar[int]

    def __post_init__(self, fio2, pao2, resp_support_count, crea, diuresis):
        self.respiration: str = resp_support_count
        self.oxygenation_index = int(pao2/fio2)
        self.crea: int = crea
        self.diuresis: int = diuresis

        path = 'program_logic/data/scales.xlsx'
        sheet = 'sofa_count'
        self.data = pd.read_excel(path, sheet_name=sheet, index_col=0, dtype=str)
        self.lethality_frame = pd.read_excel(path, sheet_name='sofa_lethal', index_col=0)

        self.total_score: int = 0

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
            if self.__dict__[indicator_name] in limits:
                return score

    def get_oxygenation_score(self) -> int:
        oxy_ser = self.get_score_scale(self.respiration)
        for score in oxy_ser.index:
            cell_data = oxy_ser[score]
            limits = Limits(
                *[fast_real(e) for e in cell_data.split()])
            if self.oxygenation_index in limits:
                return score

    def get_excretion_count(self) -> int:
        diuresis_score = self.get_score('diuresis')
        crea_score = self.get_score('crea')
        print(diuresis_score)
        match diuresis_score:
            case None:
                return crea_score
            case int(d) if d >= crea_score:
                return diuresis_score
            case int(d) if d < crea_score:
                return crea_score

    def get_scores(self):
        field_names = [i.name for i in fields(self)]
        scores = {'oxygenation': self.get_oxygenation_score()}

        for indicator_name in field_names:
            scores[indicator_name] = self.get_score(indicator_name)

        scores['excretion'] = self.get_excretion_count()
        self.total_score = sum(scores.values())

        return scores

    def get_lethality(self):
        return self.get_score('total_score')

    def __call__(self, *args, **kwargs):
        scores = self.get_scores()
        rows = ['индекс оксигенации', self.oxygenation_index]
        rows.extend([[translation_dict[i], scores[i]] for i in scores])
        rows.append(['сумма', self.total_score])
        rows.append(['летальность', self.get_lethality()])

        my_table = get_my_table_string(header=False, rows=rows)
        return my_table

