import pandas as pd
from dataclasses import dataclass, fields, InitVar
from fastnumbers import fast_real

from oac.program_logic.patientparameter import Limits
from oac.program_logic.my_table import get_my_table_string


ph2o = 47
patm_spb = 753
delta_p = float(patm_spb - ph2o)


@dataclass
class AaDO2Counter:
    age: int
    pao2: int
    fio2: float
    paco2: int
    temp: float

    def get_age_norm(self) -> float:
        return round(self.age/4, 1) + 4.0

    def get_aado2(self) -> float:
        return round((self.fio2*delta_p - self.paco2/0.8) - self.pao2, 1)

    def __call__(self, mode='', *args, **kwargs) -> float | str:
        real_aado2 = self.get_aado2()
        print(real_aado2)

        if mode == 'for_print':
            norm_aado2 = self.get_age_norm()
            rows = [
                ['результат', real_aado2],
                ['возрастная норма', norm_aado2],
                ['рaзница', round(real_aado2 - norm_aado2, 1)]
            ]

            my_table = get_my_table_string(header=False, rows=rows)
            return my_table

        else:
            return real_aado2
