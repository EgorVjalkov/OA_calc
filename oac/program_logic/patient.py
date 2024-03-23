import pandas as pd
from typing import Optional, Any, Union
from collections import defaultdict

from oac.dialog.variants_with_id import variants, topics
from oac.program_logic.blood_counter import BloodVolCounter, BleedCounter
from oac.program_logic.drag import DragCounter


class Patient:
    def __init__(self):
        self.results = defaultdict(dict)
        self.current_function_id: Optional[str] = None
        self.func: Optional[BloodVolCounter, DragCounter] = None
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

    def get_variants(self, ctx_data) -> list: # посмотри где добавить рассчетку
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

    def match_ctx_data(self, data: dict) -> object:
        self.func_id = data['func_id']

        match self.func_id, data:
            case ['blood_vol_count',
                  {'height': h, 'weight': w, 'weight_before': b}]:
                self.func = BloodVolCounter(h, w, b)

            case ['drag_count',
                  {'weight': weight}]:
                self.func = DragCounter(weight)

        self.variants_for_tg = self.get_variants(data)
        return self

    @property
    def last_result(self) -> dict:
        return list(self.results.values())[-1]

    def get_result(self):
        result = self.func()
        self.results[self.func_id].update({
            'parameters': self.func.__dict__,
            'result': result})
        self.func = None
        return result

    def extract_parameters(self, cls: object) -> dict:
        params = cls.__dict__
        variants_dict = dict(variants[self.func_id])
        translated_params = {}

        for i in params:
            translated_params[]




def func_test(patient: Patient, ctx_data: dict):
    patient.match_ctx_data(ctx_data)
    print(f'id - {ctx_data["func_id"]}')
    print(f'vars - {patient.variants_for_tg}')
    print(f'func - {patient.func}')


if __name__ == '__main__':

    pat = Patient()
    ctx = {'func_id': 'blood_vol_count'}

    pat.match_ctx_data(ctx)
    func_test(pat, ctx)

    ctx |= {'height': 170, 'weight': 70}

    pat.match_ctx_data(ctx)
    func_test(pat, ctx)

    #ctx |= {'weight_before': 63, 'func_id': 'drag_count'}
    ctx |= {'weight_before': 63}

    pat.match_ctx_data(ctx)
    print(pat.func_id)
    func_test(pat, ctx)
    res = pat.get_result()
    print(res, pat.last_result)


