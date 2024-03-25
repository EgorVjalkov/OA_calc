from typing import Optional
import pandas as pd
from dataclasses import dataclass
from prettytable import PrettyTable

from oac.program_logic.my_table import get_my_table_string


@dataclass
class Drag:
    drag: str
    dose_per_kg: str
    unit: str
    flask_dose: str
    flask_unit: str

    def __post_init__(self):
        self.dose_per_kg: float = float(self.dose_per_kg)
        self.flask_dose: float = float(self.flask_dose)
        self.patient_dose: Optional[float] = None

    def __repr__(self):
        return f'Drag: {self.drag}'

    @staticmethod
    def prepare_dose(dose):
        if dose > 10:
            return int(dose)
        else:
            return dose

    def get_patient_dose(self, weight: int) -> float:
        self.patient_dose = float(weight) * self.dose_per_kg
        return round(self.patient_dose, 1)

    def get_patient_dose_in_flasks(self):
        return round(self.patient_dose / self.flask_dose, 1)

    def count(self, weight: int) -> pd.Series:
        dose_per_kg = f'{self.prepare_dose(self.dose_per_kg)}/кг'
        dose_in_str = f'{self.prepare_dose(self.get_patient_dose(weight))}{self.unit}'
        flasks = f'{self.get_patient_dose_in_flasks()} {self.flask_unit}'
        answer = pd.Series({
            f'препарат': self.drag, 'расчет': dose_per_kg, 'доза': dose_in_str, 'ед': flasks})
        return answer


@dataclass
class DragCounter:
    weight: int

    def __call__(self, *args, **kwargs) -> str:
        path = 'drag_dosage.xlsx'
        path = 'program_logic/drag_dosage.xlsx'
        drag_frame = pd.read_excel(path, dtype=str)

        drag_list = [Drag(*drag_frame.loc[i]).count(self.weight)
                     for i in drag_frame.index]

        my_table = get_my_table_string(
            fields=['препарат', 'расчет', 'доза', 'ед'],
            rows=drag_list,
        )
        return my_table


if __name__ == '__main__':
    dd = DragCounter(89)
    rep = dd()
    print(rep)
