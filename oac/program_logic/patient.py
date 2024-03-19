import pandas as pd
from oac.program_logic.function import Function
from typing import Optional, Any
from collections import defaultdict


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
        self.func: Optional[Function] = None

    def build_func(self, func_id):
        params = self.session_data.get('parameters')
        self.func = Function(func_id, params)
        return self.func

    def update_data(self, key: str, item: dict):
        self.session_data[key].update(item)
        return self


patient = Patient()
patient.update_data('parameters', {'height': 160, 'weight': 70})
patient.update_data('parameters', {'weight_before': 63})
patient.build_func('blood_vol_count')
if patient.func.is_args_ready:
    report = patient.func()
    patient.update_data('results', {patient.func.function_key: report})
patient.update_data('parameters', {'weight_before': 73})
patient.build_func('blood_vol_count')
if patient.func.is_args_ready:
    report = patient.func()
    patient.update_data('results', {patient.func.function_key: report})
else:
    print('enough data')
print(patient.session_data)




