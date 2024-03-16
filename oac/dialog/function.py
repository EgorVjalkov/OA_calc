from oac.dialog.variants_with_id import variants, answers
from oac.program_logic.Patient2 import Patient
from oac.dialog.variants_with_id import topics


class NecessaryArgs:
    def __init__(self, for_func: str, ctx_data: dict):
        self.for_func = for_func
        self.ctx_data = ctx_data
        self.necessary_keys = [i[1] for i in variants[self.for_func]]
        self.kwargs_dict = {}

    @property
    def filtered_kwrags(self):
        self.kwargs_dict = {i: self.ctx_data[i] for i in self.ctx_data if i in self.necessary_keys}
        return self.kwargs_dict

    @property
    def is_ready(self):
        return len(self.filtered_kwrags) == len(self.necessary_keys)


class DynamicVars:
    def __init__(self, for_func: str):
        self.vars_with_id = variants[for_func].copy()

    def append_count_var(self):
        self.vars_with_id.append(('рассчитать', 'count'))


class Function:
    def __init__(self, ctx_data: dict):
        self.function_key = ctx_data.get('func_id')
        self.args = NecessaryArgs(self.function_key, ctx_data)
        self.variants = DynamicVars(self.function_key)
        self.topic = topics[self.function_key]

    def __repr__(self):
        return f'{Function}({self.function_key})'

    def get_dict_with_variants(self) -> dict:
        return {self.function_key: self.variants.vars_with_id}

    @property
    def is_args_ready(self) -> bool:
        return self.args.is_ready

    def set_btn_text(self):
        filtered_kwargs = self.args.filtered_kwrags
        for i in self.variants.vars_with_id:
            match i:
                case [btn_text, btn_id] if btn_id in filtered_kwargs:
                    ind = self.variants.vars_with_id.index(i)
                    value = filtered_kwargs[btn_id]
                    self.variants.vars_with_id[ind] = (f'{btn_text}: {value}', btn_id)

        return self.variants.vars_with_id

    def __call__(self, *args, **kwargs):
        patient = Patient(**self.args.kwargs_dict)
        patient.count_patient_data(self.function_key)
        return patient.get_report(self.function_key)


class PatientParameter:
    def __init__(self, name):
        self.name = name

    @property
    def answer(self):
        return f'Введите показатель {answers[self.name]}'


if __name__ == '__main__':
    data = {'func_id': 'blood_vol_count', 'weight': 56, 'height': 146, 'weight_before': 52}
    func = Function(data)
    if func.is_args_ready:
        func.variants.append_count_var()
        print(func.variants.vars_with_id)
        rep = func()
        print(rep)
    else:
        print('none')
