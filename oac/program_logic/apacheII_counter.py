from dataclasses import dataclass, InitVar, fields
from fastnumbers import fast_int
from typing import Dict

from oac.program_logic.AaDO2_counter import AaDO2Counter
from oac.program_logic.scale_counter import BaseScale, ScaleParam
from oac.program_logic.parameters import ShortParam
from oac.program_logic.my_table import get_my_table_string


@dataclass
class ApacheIIBase(BaseScale):
    age: ShortParam
    body_temp: ShortParam
    mean_pressure: ShortParam
    heart_rate: ShortParam
    breath_rate: ShortParam
    pH: ShortParam
    Na: ShortParam
    K: ShortParam
    crea: ShortParam
    Hct: ShortParam
    WBC: ShortParam

    glasgow: InitVar[ShortParam]
    chronic_data: InitVar[ShortParam]
    operation_data: InitVar[ShortParam]

    def __post_init__(self, glasgow, chronic_data, operation_data):
        super().__post_init__()
        self.get_scale_frame('apacheII')

        self.glasgow_param = glasgow
        self.chronic_param = chronic_data
        self.operation_param = operation_data

    def get_CHP_score(self) -> int:
        #print(self.chronic_param, self.operation_param)
        match self.chronic_param.value, self.operation_param.value:
            case 'chronic', 'elect':
                return 2
            case 'chronic', 'emerg' | 'no_oper':
                return 5
        return 0

    def get_CHP_param(self) -> ScaleParam:
        name = 'CHP'
        value = f'{self.chronic_param.value}+{self.operation_param.value}'
        score = self.get_CHP_score()
        return ScaleParam(name, value, score)

    def get_apacheII_scores(self) -> Dict[str, ScaleParam]:
        scores = self.get_simple_scores()
        scores['glasgow'] = ScaleParam(self.glasgow_param.name,
                                       self.glasgow_param.value,
                                       f'{15-self.glasgow_param.value}')
        scores['CHP'] = self.get_CHP_param()

        return scores

    def __call__(self, *args, **kwargs):
        return BaseScale.__call__(self, get_scores=self.get_apacheII_scores)


@dataclass
class ApacheIICounterFio2Less50(ApacheIIBase):
    pao2: ShortParam

    def __post_init__(self, glasgow, chronic_data, operation_data):
        super().__post_init__(glasgow, chronic_data, operation_data)


@dataclass
class ApacheIICounter(ApacheIICounterFio2Less50):
    fio2: InitVar[ShortParam]
    pao2: InitVar[ShortParam]
    paco2: InitVar[ShortParam]
    aado2: ShortParam = 0

    def __post_init__(self, glasgow, chronic_data, operation_data, fio2, pao2, paco2):
        super().__post_init__(glasgow, chronic_data, operation_data)
        #print([self.age, fio2, pao2, paco2, self.body_temp])
        args = [p.value for p in [self.age, fio2, pao2, paco2, self.body_temp]]
        self.aado2 = ShortParam('AaDO2', AaDO2Counter(*args).__call__())
