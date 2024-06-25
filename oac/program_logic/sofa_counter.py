from dataclasses import dataclass, InitVar

import pandas as pd
from fastnumbers import fast_real
from typing import Dict

from oac.program_logic.patientparameter import Limits
from oac.program_logic.scale_counter import BaseScale, ScaleParam, ShortParam
from oac.program_logic.my_table import get_my_table_string


@dataclass
class SofaCounter(BaseScale):
    fio2: InitVar[ShortParam]
    pao2: InitVar[ShortParam]
    resp_support_data: InitVar[ShortParam]
    plt: ShortParam
    bili: ShortParam
    hypotension_data: ShortParam
    glasgow: ShortParam
    crea: InitVar[ShortParam]
    diuresis: InitVar[ShortParam]

    def __post_init__(self, fio2, pao2, resp_support_data, crea, diuresis):
        super().__post_init__()
        self.get_scale_frame('sofa')

        self.respiration: ShortParam = resp_support_data
        self.oxygenation_index = int(pao2.value/fio2.value)
        self.crea: ShortParam = crea
        self.diuresis: ShortParam = diuresis

    def get_oxygenation_score(self) -> ScaleParam:
        oxy_ser = pd.Series(dtype=object)

        oxy_dict = {
            ('без поддержки', 'увл. О2'): 'no_resp_support',
            ('НИВЛ', 'ИВЛ'): 'resp_support',
        }

        for i in oxy_dict:
            if self.respiration.value in i:
                oxy_ser = self.get_score_scale(oxy_dict[i])

        for score in oxy_ser.index:
            cell_data = oxy_ser[score]
            limits = Limits(
                *[fast_real(e) for e in cell_data.split()])
            if self.oxygenation_index in limits:
                return ScaleParam(f'pao2/fio2 ({self.respiration.value})',
                                  f'{self.oxygenation_index}',
                                  score)

    def get_excretion_score(self) -> ScaleParam:
        diuresis_score: ScaleParam = self.get_score('diuresis')
        crea_score: ScaleParam = self.get_score('crea')
        match diuresis_score:
            case None:
                return crea_score
            case d if d.score >= crea_score.score:
                return diuresis_score
            case d if d.score < crea_score.score:
                return crea_score

    def get_sofa_scores(self) -> Dict[str, ScaleParam]:
        scores = {'oxygenation': self.get_oxygenation_score()}
        scores.update(self.get_simple_scores())
        scores['excretion'] = self.get_excretion_score()
        return scores

    def __call__(self, *args, **kwargs):
        return BaseScale.__call__(self, self.get_sofa_scores)
