from dataclasses import dataclass, InitVar
from fastnumbers import fast_real

from oac.program_logic.patientparameter import Limits
from oac.program_logic.scale_counter import BaseScale, translation_dict
from oac.program_logic.my_table import get_my_table_string


@dataclass
class SofaCounter(BaseScale):
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
        super().__post_init__()
        self.get_scale_frame('sofa')

        self.respiration: str = resp_support_count
        self.oxygenation_index = int(pao2/fio2)
        self.crea: int = crea
        self.diuresis: int = diuresis

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

    def get_sofa_scores(self):
        scores = {'oxygenation': self.get_oxygenation_score()}
        scores.update(self.get_simple_scores())
        scores['excretion'] = self.get_excretion_count()

        self.total_score = sum(scores.values())

        return scores

    def __call__(self, *args, **kwargs):
        scores = self.get_sofa_scores()
        rows = [['индекс оксигенации', self.oxygenation_index]]
        rows.extend([[translation_dict[i], scores[i]] for i in scores])
        rows.append(['сумма', self.total_score])
        rows.append(['летальность', self.get_lethality()])

        my_table = get_my_table_string(header=False, rows=rows)
        return my_table
