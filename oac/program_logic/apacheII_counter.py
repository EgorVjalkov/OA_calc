from dataclasses import dataclass, InitVar
from fastnumbers import fast_int

from oac.program_logic import AaDO2_counter
from oac.program_logic.scale_counter import BaseScale, translation_dict
from oac.program_logic.my_table import get_my_table_string
from oac.program_logic.parameters import ShortParam


@dataclass
class ApacheIICounterFio2Less50(BaseScale):
    age: ShortParam
    body_temp: ShortParam
    mean_pressure: ShortParam
    heart_rate: ShortParam
    breath_rate: ShortParam
    pao2: ShortParam
    pH: ShortParam
    Na: ShortParam
    K: ShortParam
    crea: ShortParam
    Hct: ShortParam
    WBC: ShortParam

    glasgow: InitVar[ShortParam]
    chronic_var: InitVar[ShortParam]
    operation_var: InitVar[ShortParam]

    def __post_init__(self, glasgow, chronic_var, operation_var):
        super().__post_init__()
        self.get_scale_frame('apacheII')

        self.glasgow_param = glasgow
        self.chronic_param = chronic_var
        self.operation_param = operation_var

    def get_CHP_score(self) -> int:
        match self.chronic_param.count, self.operation_param.count:
            case 'chronic', 'elect':
                return 2
            case 'chronic', 'emerg' | 'no_oper':
                return 5
        return 0

    def get_apacheII_scores(self):
        scores = self.get_simple_scores()
        scores['glasgow'] = self.glasgow_param.value
        scores['CHP'] = self.get_CHP_score()
        scores = {i: fast_int(scores[i]) for i in scores}

        self.total_score = sum(scores.values())

        return scores

    def __call__(self, *args, **kwargs):
        scores = self.get_apacheII_scores()
        rows = [, scores[i]] for i in scores]
        rows.append(['сумма', self.total_score])
        rows.append(['летальность', self.get_lethality()])

        my_table = get_my_table_string(header=False, rows=rows)
        return my_table



