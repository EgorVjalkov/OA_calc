from typing import Optional
import pandas as pd
from dataclasses import dataclass, InitVar

from oac.program_logic.my_table import get_my_table_string
from oac.program_logic.patientparameter import Limits


@dataclass
class BaseDrag:
    drag: str
    dose: str

    def __post_init__(self):
        self.dose: float = float(self.dose)
        self.patient_dose: Optional[float] = None

    def get_patient_dose(self, weight: int) -> float:
        print(self)
        self.patient_dose = float(weight) * self.dose
        return round(self.patient_dose, 1)


@dataclass
class DragInjection(BaseDrag):
    unit: str
    flask_dose: str
    flask_unit: str

   # def __post_init__(self):
   #     self.flask_dose: float = float(self.flask_dose)

    def __repr__(self):
        return f'Drag: {self.drag}'

    @staticmethod
    def prepare_dose(dose):
        if dose > 10:
            return int(dose)
        else:
            return dose

    def get_patient_dose_in_flasks(self):
        return round(self.patient_dose / self.flask_dose, 1)

    def count(self, weight: int) -> pd.Series:
        dose_per_kg = f'{self.prepare_dose(self.dose)}/кг'
        dose_in_str = f'{self.prepare_dose(self.get_patient_dose(weight))}{self.unit}'
        flasks = f'{self.get_patient_dose_in_flasks()} {self.flask_unit}'
        answer = pd.Series({
            f'препарат': self.drag, 'расчет': dose_per_kg, 'доза': dose_in_str, 'ед': flasks})
        return answer


@dataclass
class DragInfusion(BaseDrag):
    concentration: InitVar[str]
    d_limit: InitVar[str]
    drag_id: str

    def __post_init__(self, concentration, d_limit):
        self.concentration: float = float(concentration)
        limits = [float(i) for i in d_limit.split()]
        self.d_limit: Limits = Limits(limits[0], limits[1])


@dataclass
class DragCounter:
    weight: int
    func_id: str

    def load_frame(self):
        path = 'program_logic/data/drag_dosage.xlsx'
        drag_frame = pd.read_excel(path, sheet_name=self.func_id, dtype=str)
        return drag_frame

    def __call__(self, *args, **kwargs) -> str:
        drag_frame = self.load_frame()

        drag_list = [DragInjection(*drag_frame.loc[i]).count(self.weight)
                     for i in drag_frame.index]

        my_table = get_my_table_string(
            fields=['препарат', 'расчет', 'доза', 'ед'],
            rows=drag_list,
        )
        return my_table


if __name__ == '__main__':
    #drag = BaseDrag('na', '10')
    drag = DragInjection('na', '10', 'mg', '500', 'fl')
    print(drag.dose)
    print(drag.get_patient_dose(76))

