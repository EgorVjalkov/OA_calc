import dataclasses
from dataclasses import dataclass, InitVar
from typing import Optional, Dict, NamedTuple, Type
from collections import namedtuple

import pandas as pd


Btn = namedtuple('Btn', 'text id')


@dataclass
class Limits:
    min: int
    max: int

    def __contains__(self, item: int):
        if self.min <= item <= self.max:
            return True
        else:
            return False


@dataclass
class CompParamMenuBtn:
    id: str
    btn: str
    text_if_filled: str
    sma_risk_factor_count: int

    def make_button(self):
        return Btn(self.btn, self.id)


@dataclass
class BaseParameter:
    id: str
    func_ids: str
    btn_text: str
    btn_text_filled: str
    fill_by_text_input: bool
    _topic: str
    default_value: [int | str]

    def __post_init__(self):
        self.fill_by_text_input = bool(self.fill_by_text_input)

    @property
    def value(self):
        return self.default_value

    @value.setter
    def value(self, new_value):
        self.default_value = new_value

    @property
    def topic(self):
        return self._topic


@dataclass
class PatientParameter(BaseParameter):
    limits: InitVar[str]

    def __post_init__(self, limits):
        l_list = [int(i) for i in limits.split()]
        self.limits: Limits = Limits(*l_list)

    def __repr__(self):
        return f'PatientParameter({self.id}={self.default_value})'

    @property
    def value(self):
        return self.default_value

    @value.setter
    def value(self, new_value):
        self.default_value = new_value

    @property
    def topic(self):
        return f'{self._topic}. Допустимые значения в интервале от {self.limits.min} до {self.limits.max}.'

    @property
    def button_text(self):
        if self.value:
            return self.btn_text_filled.format(self.value)
        else:
            return self.btn_text


@dataclass
class ComplexParameter(BaseParameter):
    variants: Optional[Dict[str, CompParamMenuBtn]] = None

    def __repr__(self):
        return f'ComplexParameter({self.id}={self.default_value})'

    @property
    def count(self):
        return self.variants[self.value].sma_risk_factor_count

    @property
    def button_text(self):
        if self.value:
            variant = self.variants[self.value]
            return self.btn_text_filled.format(variant.text_if_filled)
        else:
            return self.btn_text

    def get_btns(self):
        return [i.make_button() for i in self.variants.values()]


def load_parameters() -> dict:
    params_dict = {}
    # path = 'parameters.xlsx'
    path = 'program_logic/data/parameters.xlsx'
    param_df = pd.read_excel(path, sheet_name='parameters', dtype=object)
    comp_param_btns_df = pd.read_excel(path, sheet_name='parameter_menu', dtype=object)
    # filtered = param_df.func_id.map(lambda i: func_id in i)
    # param_df = param_df[filtered == True]
    # del param_df['func_id']

    for param_row in param_df.index:
        row = param_df.loc[param_row]
        if row.fill_by_text_input:
            parameter = PatientParameter(**row.to_dict())
        else:
            variants = comp_param_btns_df[comp_param_btns_df.parameter_id == row.id]
            del variants['parameter_id']
            variants = [CompParamMenuBtn(**variants.loc[i].to_dict()) for i in variants.index]

            row_dict = row.to_dict()
            row_dict.update({'variants': {i.id: i for i in variants}})

            cls_fields = [i.name for i in dataclasses.fields(ComplexParameter)]
            parameter = ComplexParameter(*[row_dict[i] for i in row_dict if i in cls_fields])
        print(parameter)

        params_dict[parameter.id] = parameter
    return params_dict

