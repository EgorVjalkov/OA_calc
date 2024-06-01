import dataclasses
from dataclasses import dataclass, InitVar
from typing import Optional, Dict, NamedTuple, Type
from collections import namedtuple
from datetime import datetime

import pandas as pd


Btn = namedtuple('Btn', 'text id')


@dataclass
class Limits:
    min: int | float
    max: int | float

    def __contains__(self, item: int | float):
        return self.min <= item <= self.max


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
    default_value: [int | str | datetime]

    def __post_init__(self):
        self.fill_by_text_input = bool(self.fill_by_text_input)

    def __repr__(self):
        return f'BaseParameter({self.id}={self.default_value})'

    @property
    def value(self):
        return self.default_value

    @value.setter
    def value(self, new_value):
        self.default_value = new_value

    @property
    def topic(self):
        return self._topic

    @property
    def button_text(self):
        if self.value:
            return self.btn_text_filled.format(self.value)
        else:
            return self.btn_text


@dataclass
class DateTimeParameter(BaseParameter):

    def __post_init__(self):
        self._datetime: Optional[datetime] = None

    def __repr__(self):
        return f'DateTimeParameter({self.id}={self.default_value})'

    @property
    def value_like_datetime(self) -> datetime:
        return self._datetime

    @value_like_datetime.setter
    def value_like_datetime(self, value: datetime) -> None:
        self._datetime = value


@dataclass
class LimitedParameter(BaseParameter):
    limits: str

    def __post_init__(self):
        match self.limits:
            case limit_str if '.' in limit_str:
                l_list = [float(i) for i in limit_str.split(' ')]

            case limit_str:
                l_list = [int(i) for i in limit_str.split()]

        self.limits: Limits = Limits(*l_list)

    def __repr__(self):
        return f'LimitedParameter({self.id}={self.default_value})'

    @property
    def topic(self):
        return f'{self._topic}. Допустимые значения в интервале от {self.limits.min} до {self.limits.max}.'


@dataclass
class SelectedParameter(BaseParameter):
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


def init_example_by_fields(cls, kwargs_dict) -> BaseParameter:
    cls_fields = [i.name for i in dataclasses.fields(cls)]
    print([kwargs_dict[i] for i in kwargs_dict if i in cls_fields])
    return cls(*[kwargs_dict[i] for i in kwargs_dict if i in cls_fields])


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
        parameter = None
        row_dict = param_df.loc[param_row].to_dict()
        print(row_dict['id'], row_dict['fill_by_text_input'], row_dict['limits'])

        match row_dict:
            case {'fill_by_text_input': 1, 'limits': 'no limits'}:
                parameter = init_example_by_fields(BaseParameter, row_dict)

            case {'fill_by_text_input': 1}:
                parameter = init_example_by_fields(LimitedParameter, row_dict)

            case {'fill_by_text_input': 'datetime'}:
                parameter = init_example_by_fields(DateTimeParameter, row_dict)

            case {'fill_by_text_input': 0}:
                variants = comp_param_btns_df[comp_param_btns_df.parameter_id == row_dict['id']]
                variants = [init_example_by_fields(CompParamMenuBtn, variants.loc[i].to_dict())
                            for i in variants.index]
                #variants = [CompParamMenuBtn(**variants.loc[i].to_dict()) for i in variants.index]
                row_dict.update({'variants': {i.id: i for i in variants}})
                parameter = init_example_by_fields(SelectedParameter, row_dict)
            case _:
                print('error')
        print(parameter)
        params_dict[parameter.id] = parameter

    return params_dict

