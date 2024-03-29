from dataclasses import dataclass
from typing import Optional

import pandas as pd


@dataclass
class Btn:
    text: str
    id: str


@dataclass
class PatientParameter:
    id: str
    btn_text: str
    btn_text_filled: str
    fill_by_text_input: bool
    topic: str
    default_value: Optional[int | str] = None

    def __post_init__(self):
        self.fill_by_text_input = bool(self.fill_by_text_input)

    @property
    def value(self):
        return self.default_value

    @value.setter
    def value(self, new_value):
        self.default_value = new_value

    @property
    def button_text(self):
        if self.value:
            return self.btn_text_filled.format(self.value)
        else:
            return self.btn_text


def load_parameters(func_id) -> dict:
    params_dict = {}
    # path = 'parameters.xlsx'
    path = 'dialog/parameters.xlsx'
    param_df = pd.read_excel(path, sheet_name='parameters', dtype=object)
    filtered = param_df.func_id.map(lambda i: func_id in i)
    param_df = param_df[filtered == True]
    del param_df['func_id']

    for param_row in param_df.index:
        row = param_df.loc[param_row]
        parameter = PatientParameter(**row.to_dict())
        params_dict[parameter.id] = parameter
    return params_dict

