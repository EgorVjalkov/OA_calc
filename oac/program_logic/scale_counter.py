import pandas as pd
from dataclasses import dataclass, fields
from fastnumbers import fast_real

from oac.program_logic.patientparameter import Limits


@dataclass
class SofaCounter:
    fio2: float | int
    pao2: int
    respiration: str
    plt: int
    bili: int
    hypotension: int
    glasgow: int
    crea: int
    diuresis: int

    def __post_init__(self):
        path = 'program_logic/data/scales.xlsx'
        sheet = 'sofa_count'
        self.data = pd.read_excel(path, sheet_name=sheet, index_col=0, dtype=str)
        self.oxygenation_index = int(self.pao2 / self.fio2)

    def get_score_scale(self, indicator_name: str) -> pd.Series:
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
        for i in [self.crea, self.diuresis]:
            ind_name = fields(self)

            oxy_ser = self.data.loc[self.respiration]
            oxy_ser = oxy_ser[oxy_ser.map(pd.notna) == True]

    def get_scores(self):
        field_names = [i.name for i in fields(self)]
        scores = {}

        for indicator_name in self.data.index:
            if indicator_name in field_names:
                scores[indicator_name] = self.get_score(indicator_name)

        scores['oxygenation'] = self.get_oxygenation_score()




