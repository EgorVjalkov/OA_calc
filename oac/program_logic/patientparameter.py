from typing import Optional, Dict, Union, Any
from collections import namedtuple
from datetime import datetime
from fastnumbers import fast_real
from pydantic import BaseModel, Field, model_validator

from oac.program_logic.data_loader import data_loader
Btn = namedtuple('Btn', 'text id')


class Limits(BaseModel):
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


class CompParamMenuBtn(BaseModel):
    id: str
    btn: str
    text_if_filled: str
    data: Union[str, int]

    def make_button(self):
        return Btn(self.btn, self.id)


class BaseParameter(BaseModel):
    id: str
    func_ids: str
    btn_text: str
    btn_text_filled: str
    fill_by_text_input: str
    topic_data: str = Field(alias='_topic')
    default_value: Any

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
        return self.topic_data

    @property
    def button_text(self):
        value = fast_real(self.value)
        if not value:
            return self.btn_text
        else:
            return self.btn_text_filled.format(self.value)


class DateTimeParameter(BaseParameter):
    default_value: Any = ''
    datetime_: Optional[datetime] = None

    def __repr__(self):
        return f'DateTimeParameter({self.id}={self.default_value})'

    @property
    def value_like_datetime(self) -> datetime:
        return self.datetime_

    @value_like_datetime.setter
    def value_like_datetime(self, value: datetime) -> None:
        self.datetime_ = value


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


class NumericParameter(BaseParameter):
    ndigits: int = 0

    @model_validator(mode='after')
    def set_ndigits(self):
        val_str = str(self.default_value)
        if len(val_str) > 1:
            self.ndigits = len(val_str.replace('0.', ''))
        else:
            self.ndigits = 0
        return self

    def __repr__(self):
        return f'NumericParameter({self.id}={self.default_value})'

    @property
    def value(self):
        return self.default_value

    @value.setter
    def value(self, new_value):
        self.default_value = round(fast_real(new_value), self.ndigits)


class LimitedParameter(NumericParameter):
    limits_str: str = Field(alias='limits')
    parsed_limits: Optional[Limits] = None

    @model_validator(mode='after')
    def parse_limits(self):
        if '.' in self.limits_str:
            l_list = [float(i) for i in self.limits_str.split(' ')]
        else:
            l_list = [int(i) for i in self.limits_str.split()]
        self.parsed_limits = Limits(min=l_list[0], max=l_list[1] if len(l_list) > 1 else None)
        return self

    @property
    def limits(self) -> Limits:
        return self.parsed_limits

    def __repr__(self):
        return f'LimitedParameter({self.id}={self.default_value})'

    @property
    def topic(self):
        return f'{self.topic_data}. Допустимые значения в интервале от {self.parsed_limits.min} до {self.parsed_limits.max}.'

def init_example_by_fields(cls, kwargs_dict) -> BaseParameter:
    return cls(**kwargs_dict)


def load_parameters() -> dict:
    params_dict = {}
    data = data_loader.parameters_data
        
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
