import dataclasses
from dataclasses import dataclass, InitVar
from typing import Optional, Dict, Union
from collections import namedtuple
from datetime import datetime
from fastnumbers import fast_real

import json
from pathlib import Path


Btn = namedtuple('Btn', 'text id')


@dataclass
class Limits:
    min: int | float
    max: Optional[int | float | str] = None

    @property
    def is_ray_limit(self) -> bool:
        return self.max == 'inf'

    @property
    def is_point_limit(self) -> bool:
        return self.max is None

    def __contains__(self, item: int | float):
        if self.is_ray_limit:
            return self.min <= item
        if self.is_point_limit:
            return self.min == item
        return self.min <= item <= self.max


@dataclass
class CompParamMenuBtn:
    id: str
    btn: str
    text_if_filled: str
    data: str

    def make_button(self):
        return Btn(self.btn, self.id)


@dataclass
class BaseParameter:
    id: str
    func_ids: str
    btn_text: str
    btn_text_filled: str
    fill_by_text_input: str
    _topic: str
    default_value: str

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
        value = fast_real(self.value)
        if not value:
            return self.btn_text
        else:
            return self.btn_text_filled.format(self.value)


@dataclass
class DateTimeParameter(BaseParameter):

    def __post_init__(self):
        self.default_value = ''
        self.datetime_: Optional[datetime] = None

    def __repr__(self):
        return f'DateTimeParameter({self.id}={self.default_value})'

    @property
    def value_like_datetime(self) -> datetime:
        return self.datetime_

    @value_like_datetime.setter
    def value_like_datetime(self, value: datetime) -> None:
        self.datetime_ = value


@dataclass
class SelectedParameter(BaseParameter):
    variants: Optional[Dict[str, CompParamMenuBtn]] = None

    def __repr__(self):
        return f'SelectedParameter({self.id}={self.default_value})'

    @property
    def data(self) -> str:
        return self.variants[self.value].data

    @property
    def button_text(self):
        if self.value:
            variant = self.variants[self.value]
            return self.btn_text_filled.format(variant.text_if_filled)
        else:
            return self.btn_text

    def get_btns(self):
        return [i.make_button() for i in self.variants.values()]


@dataclass
class NumericParameter(BaseParameter):

    def __post_init__(self):
        val_str = str(self.default_value)
        if len(val_str) > 1:
            self.ndigits = len(val_str.replace('0.', ''))
        else:
            self.ndigits = 0

    def __repr__(self):
        return f'NumericParameter({self.id}={self.default_value})'

    @property
    def value(self):
        return self.default_value

    @value.setter
    def value(self, new_value):
        self.default_value = round(new_value, self.ndigits)


@dataclass
class LimitedParameter(NumericParameter):
    limits: str

    def __post_init__(self):
        super().__post_init__()
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


def init_example_by_fields(cls, kwargs_dict) -> BaseParameter:
    cls_fields = [i.name for i in dataclasses.fields(cls)]
    return cls(*[kwargs_dict.get(i) for i in cls_fields])


def load_parameters() -> dict:
    params_dict = {}
    path = Path(__file__).parent / 'data' / 'parameters.json'
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    param_dict_data = data.get('parameters', {})
    comp_param_btns_data = data.get('parameter_menu', {})

    for param_id, row_dict in param_dict_data.items():
        parameter = None
        row_dict['id'] = param_id

        match row_dict:
            case {'fill_by_text_input': 'True', 'limits': l} if l in ('no limits', None):
                parameter = init_example_by_fields(NumericParameter, row_dict)

            case {'fill_by_text_input': 'True'}:
                parameter = init_example_by_fields(LimitedParameter, row_dict)

            case {'fill_by_text_input': 'datetime'}:
                parameter = init_example_by_fields(DateTimeParameter, row_dict)

            case {'fill_by_text_input': 'False'}:
                variants = []
                for k, v in comp_param_btns_data.items():
                    if v.get('parameter_id') == row_dict['id']:
                        v['id'] = k
                        variants.append(init_example_by_fields(CompParamMenuBtn, v))
                row_dict.update({'variants': {i.id: i for i in variants}})
                parameter = init_example_by_fields(SelectedParameter, row_dict)
            case _:
                print('error')
        #print(parameter)
        params_dict[parameter.id] = parameter

    return params_dict
