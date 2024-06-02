import pandas as pd
from dataclasses import dataclass, fields
from fastnumbers import fast_real

from oac.program_logic.patientparameter import Limits


@dataclass
class SofaCounter:
    fio2: float | int
    pao2: int
    resp_support: str
    plt: int
    bili: int
    hypotension: int
    glasgow: int
    crea: int
    diuresis: int

    def __post_init__(self):
        path = 'program_logic/data/scales.xlsx'
        sheet = 'sofa_count'
        self.data = pd.read_excel(path, sheet_name=sheet, index_col=0)
        self.oxygenation_index = int(self.pao2 / self.fio2)

    def get_oxygenation_count(self) -> int:
        oxy_ser = self.data.loc[self.resp_support]
        oxy_ser = oxy_ser[oxy_ser.map(pd.notna) == True]

        for i in oxy_ser.index:
            cell_data = oxy_ser[i]
            limits = Limits(
                *[fast_real(e) for e in cell_data.split()])
            if self.oxygenation_index in limits:
                return i


