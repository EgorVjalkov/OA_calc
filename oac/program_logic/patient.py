import pandas as pd
from typing import Optional, Any
from collections import defaultdict

from oac.program_logic.function import Function
from oac.dialog.variants_with_id import variants
from oac.program_logic.blood_counter import BloodVolCounter, BleedCounter
from oac.program_logic.drag import DragCounter


class UserList(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def overwrite(self, item):
        if item in self:
            index = self.index(item)
            del self[index]
        self.append(item)


class Patient:
    def __init__(self):
        self.session_data = defaultdict(dict)
        self.current_function_id: Optional[str] = None
        self._func: Any = None
        self._vars: Optional[list] = None

    @property
    def func_id(self) -> str:
        return self.current_function_id

    @func_id.setter
    def func_id(self, func_id) -> None:
        self.current_function_id = func_id

    @property
    def parameters(self) -> dict:
        return self.session_data.get('parameters')

    @property
    def variants_for_tg(self) -> list:
        return self._vars

    @variants_for_tg.setter
    def variants_for_tg(self, new_vars):
        self._vars = new_vars

    def func_is_ready(self):
        return self._func is not None

    def get_variants(self, ctx_data) -> list: # посмотри где добавить рассчетку
        variants_for_tg = variants[self.func_id].copy()
        for i in variants_for_tg:
            match i:
                case [btn_text, btn_id] if btn_id in ctx_data:
                    ind = variants_for_tg.index(i)
                    value = ctx_data[btn_id]
                    variants_for_tg[ind] = (f'{btn_text}: {value}', btn_id)

        self.variants_for_tg = variants_for_tg
        return self.variants_for_tg

    def match_ctx_data(self, data: dict) -> object:
        match self.func_id, data:
            case [None, {'func_id': func_id}]: # <- соответствует выбору функции
                self.func_id = func_id
                self.variants_for_tg = self.get_variants(data)
                return self

            case ['blood_vol_count',
                  {'height': h, 'weight': w, 'weight_before': b}]:
                self._func = BloodVolCounter(h, w, b)

            case ['drag_count',
                  {'weight': weight}]:
                self._func = DragCounter(weight)

            case [func_id, ctx_data] if func_id:  # <- соответтствует заполнению даты
                self.variants_for_tg = self.get_variants(ctx_data)
                return self

    def get_finish_vars(self) -> list:
        menu_list = self.variants_for_tg
        menu_list.append(('рассчитать', 'count'))
        self.variants_for_tg = menu_list
        return self.variants_for_tg

    def update_data(self, key: str, item: dict):
        self.session_data[key].update(item)
        return self


if __name__ == '__main__':

    patient = Patient()

    ctx = {'func_id': 'blood_vol_count'}

    patient.match_ctx_data(ctx)
    print(patient.func_id)
    print(patient.variants_for_tg)
    print(patient._func)

    ctx |= {'height': 170, 'weight': 70}

    patient.match_ctx_data(ctx)
    print(patient.func_id)
    print(patient.variants_for_tg)
    print(patient._func)

    ctx |= {'weight_before': 63, 'func_id': 'drag_count'}
    # замуть со сменой функции. на доработку!!!

    patient.match_ctx_data(ctx)
    print(patient.func_id)
    print(patient.variants_for_tg)
    print(patient._func)

