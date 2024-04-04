from dataclasses import dataclass
from typing import Optional, Dict

from oac.program_logic.patientparameter import load_parameters, Btn, PatientParameter, ComplexParameter


@dataclass
class ParametersForCurrentFunc:
    current_params: Optional[dict] = None
    current_parameter_id: Optional[str] = None

    def __post_init__(self):
        self.data: Dict[str, PatientParameter] = load_parameters()

    def set_current_params(self, func_id) -> dict:
        self.current_params = {i: self.data[i] for i in self.data
                               if func_id in self.data[i].func_ids}
        return self.current_params

    def get_values(self):
        values = {}
        for i in self.current_params:
            match self.current_params[i]:
                case ComplexParameter():
                    values[f'{i}_count'] = self.current_params[i].count
                case PatientParameter():
                    values[i] = self.current_params[i].value
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
    def current(self) -> PatientParameter | ComplexParameter:
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
