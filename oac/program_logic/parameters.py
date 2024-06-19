from dataclasses import dataclass
from typing import Optional, Dict
from collections import namedtuple

from oac.program_logic.patientparameter import (load_parameters, Btn,
                                                LimitedParameter, SelectedParameter, BaseParameter)


ShortParam = namedtuple('ShortParam', 'name value')


@dataclass
class ParametersForCurrentFunc:
    current_params: Optional[dict] = None
    current_parameter_id: Optional[str] = None

    def __post_init__(self):
        self.data: Dict[str, BaseParameter] = load_parameters()

    def set_current_params(self, func_id) -> dict:
        self.current_params = {i: self.data[i] for i in self.data
                               if func_id in self.data[i].func_ids}
        return self.current_params

    def get_values(self, like: str = '') -> dict:
        values = {}
        for i in self.current_params:
            match like, self.current_params[i]:
                case 'short_params', param:
                    if isinstance(param, SelectedParameter):
                        values[f'{i}_data'] = ShortParam(param.btn_text, param.data)
                    else:
                        values[i] = ShortParam(param.btn_text, param.value)

                case '', param:
                    if isinstance(param, SelectedParameter):
                        values[f'{i}_data'] = param.data
                    else:
                        values[i] = param.value

        print(values)
        return values

    def extract(self):
        return {i: self.current_params[i].button_text for i in self.current_params}

    @property
    def parameter_id(self):
        return self.current_parameter_id

    @parameter_id.setter
    def parameter_id(self, param_id_from_tg: str) -> None:
        self.current_parameter_id = param_id_from_tg

    @property
    def current(self) -> BaseParameter:
        return self.data.get(self.current_parameter_id)

    @property
    def all_params_filled(self) -> bool:
        values = [i for i in self.current_params if not self.current_params[i].value]
        return len(values) == 0

    def get_btns(self) -> list:
        btns_list = [Btn(self.data[i].button_text, i) for i in self.current_params]
        if self.all_params_filled:
            btns_list.append(Btn('рассчитать', 'count'))
        return btns_list
