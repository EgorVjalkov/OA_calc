import pandas as pd
from dataclasses import dataclass, fields


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
        oxy_count = 'не получилося'
        oxy_ser = self.data.loc['oxygenation']
        for i in oxy_ser.index:
            oxy_index_comparison, resp_support = oxy_ser[i].split(', ')
            compar_in_str = f'{self.oxygenation_index} {oxy_index_comparison}'
            if eval(compar_in_str):
                if self.resp_support == resp_support:
                    oxy_count = oxy_ser[i]
                    print(oxy_ser[i], i)
        return oxy_count
