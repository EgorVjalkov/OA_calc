from typing import Optional, Dict, KeysView
from collections import defaultdict
from dataclasses import dataclass

from oac.dialog.variants_with_id import variants, topics
from oac.program_logic.blood_counter import BloodVolCounter
from oac.program_logic.drag import DragCounter
from oac.dialog.patientparameter import PatientParameter, load_parameters, Btn


@dataclass
class ParametersForCurrentFunc:
    func_id: str
    current_parameter_id: Optional[str] = None

    def __post_init__(self):
        self.data: Dict[str, PatientParameter] = load_parameters(self.func_id)

    @property
    def parameter_id(self):
        return self.current_parameter_id

    @parameter_id.setter
    def parameter_id(self, param_id_from_tg: str) -> None:
        self.current_parameter_id = param_id_from_tg

    @property
    def current(self) -> PatientParameter:
        return self.data.get(self.current_parameter_id)

    @property
    def necessary_params(self) -> KeysView:
        return self.data.keys()

    @property
    def all_params_filled(self) -> bool:
        values = [i for i in self.data if not self.data[i].value]
        return len(values) == 0

    def get_btns(self) -> list:
        btns_list = [Btn(self.data[i].button_text, i) for i in self.data]
        if self.all_params_filled:
            btns_list.append(Btn('рассчитать', 'count'))
        return btns_list


class Patient:
    def __init__(self):
        self.current_function_id: Optional[str] = None
        self.params: Optional[ParametersForCurrentFunc] = None
        self.func: Optional[BloodVolCounter | DragCounter] = None
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

    @property
    def topic(self):
        return topics[self.func_id]

    @property
    def func_is_ready(self):
        return self.func is not None

    def load_parameters(self) -> ParametersForCurrentFunc:
        self.params = ParametersForCurrentFunc(self.func_id)
        return self.params

    def match_ctx_data(self, data: dict) -> object:
        match self.func_id, data:
            case ['blood_vol_count',
                  {'height': h, 'weight': w, 'weight_before': b}]:
                self.func = BloodVolCounter(h, w, b)

            case ['drag_count',
                  {'weight': weight}]:
                self.func = DragCounter(weight)

        self.variants_for_tg = self.get_variants(data)
        return self

    def get_variants(self, ctx_data) -> list:
        variants_for_tg = variants[self.func_id].copy()
        for i in variants_for_tg:
            match i:
                case [btn_text, btn_id] if btn_id in ctx_data:
                    ind = variants_for_tg.index(i)
                    value = ctx_data[btn_id]
                    variants_for_tg[ind] = (f'{btn_text}: {value}', btn_id)

        if self.func_is_ready:
            variants_for_tg.append(('рассчитать', 'count'))

        return variants_for_tg

    def get_result(self) -> list:
        result = self.func()
        params = self.extract_parameters()
        self.results[self.func_id].update({
            'parameters': params,
            'result': result})
        self.func = None
        return result

    def extract_parameters(self) -> dict:
        params = self.func.__dict__
        variants_dict = dict(variants[self.func_id])
        print(variants_dict)
        translated_params = {i: params[variants_dict[i]]
                             for i in variants_dict}

        # translated_params = [f"{i} - {translated_params[i]}" for i in translated_params]
        return translated_params

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
            params = [f"{i} - {params[i]}" for i in params]
            answer.extend(list(params))
            answer.append('получены результаты:')
            result = self.results[result]['result']
            answer.append(result)
            answer.append('')
        return '\n'.join(answer)

    @property
    def is_results_empty(self):
        return len(self.results) == 0


def func_test(patient: Patient, ctx_data: dict):
    patient.match_ctx_data(ctx_data)
    print(f'id - {ctx_data["func_id"]}')
    print(f'vars - {patient.variants_for_tg}')
    print(f'func - {patient.func}')


if __name__ == '__main__':

    pat = Patient()
    pat.func_id = 'blood_vol_count'
    pat.load_parameters()
    pat.params.parameter_id = 'weight'
    pat.params.current.value = 100
    print(pat.params.current)

