from typing import Optional
from collections import defaultdict

from oac.dialogs.variants_with_id import topics
from oac.program_logic.parameters import ParametersForCurrentFunc
from oac.program_logic.blood_counter import BloodVolCounter, BleedCounter
from oac.program_logic.drag import PerWeightCounter
from oac.program_logic.sma import SmaCounter
from oac.program_logic.sofa_counter import SofaCounter
from oac.program_logic.apacheII_counter import ApacheIICounterFio2Less50


class Patient:
    def __init__(self):
        self.current_function_id: Optional[str] = None
        self.params = ParametersForCurrentFunc()
        self.func: Optional[BloodVolCounter | PerWeightCounter | SmaCounter] = None
        self.results = defaultdict(dict)

        self.variants_for_tg: Optional[list] = None

    def __repr__(self):
        if self.func_id:
            return f'Patient({self.func_id})'
        else:
            return f'Patient(new)'

    @property
    def func_id(self) -> str:
        return self.current_function_id

    @func_id.setter
    def func_id(self, func_id) -> None:
        self.current_function_id = func_id

    def set_current_params(self):
        return self.params.set_current_params(self.func_id)

    @property
    def topic(self):
        return topics[self.func_id]

    def change_func(self) -> object:

        match self.func_id:
            case 'blood_vol_count':
                self.func = BloodVolCounter(**self.params.get_values())
            case 'bleed_%_count':
                self.func = BleedCounter(**self.params.get_values())
            case 'drag_count':
                self.func = PerWeightCounter(self.func_id, **self.params.get_values())
            case 'sma_count':
                self.func = SmaCounter(**self.params.get_values())
            case 'sofa_count':
                self.func = SofaCounter(**self.params.get_values(like='short_params'))
            case 'apacheII_count':
                self.func = ApacheIICounterFio2Less50(**self.params.get_values(like='short_params'))

        return self

    def get_result(self) -> list:
        result = self.func()
        params = self.params.extract()
        self.results[self.func_id].update({
            'parameters': params,
            'result': result})
        self.func = None   # ???
        return result

    def get_reports(self, last: bool = False) -> str:
        answer = []

        result_keys = list(self.results.keys())
        if last:
            result_keys = [result_keys[-1]]
        else:
            answer.append("Ваши результаты.")

        for result in result_keys:
            answer.append("Для пациента с параметрами:")
            params = self.results[result]['parameters']
            answer.extend(list(params.values()))
            answer.extend(['', 'получены результаты:'])
            result = self.results[result]['result']
            answer.append(result)
            answer.append('')
        return '\n'.join(answer)

    @property
    def is_results_empty(self):
        return len(self.results) == 0
