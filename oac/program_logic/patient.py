from typing import Optional
from collections import defaultdict

from oac.dialog.variants_with_id import topics
from oac.program_logic.parameters import ParametersForCurrentFunc
from oac.program_logic.blood_counter import BloodVolCounter, BleedCounter
from oac.program_logic.drag import DragCounter
from oac.program_logic.sma import SmaCounter


class Patient:
    def __init__(self):
        self.current_function_id: Optional[str] = None
        self.params = ParametersForCurrentFunc()
        self.func: Optional[BloodVolCounter | DragCounter | SmaCounter] = None
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
        values = self.params.get_values()

        match self.func_id:
            case 'blood_vol_count':
                self.func = BloodVolCounter(**values)
            case 'bleed_%_count':
                self.func = BleedCounter(**values)
            case 'drag_count':
                self.func = DragCounter(**values)
            case 'sma_count':
                self.func = SmaCounter(**values)

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
            answer.append('получены результаты:')
            result = self.results[result]['result']
            answer.append(result)
            answer.append('')
        return '\n'.join(answer)

    @property
    def is_results_empty(self):
        return len(self.results) == 0
