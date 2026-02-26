from typing import Optional
import json
from pathlib import Path
from dataclasses import dataclass, InitVar

from oac.program_logic.my_table import get_my_table_string
from oac.program_logic.patientparameter import Limits


@dataclass
class BaseDrag:
    drag: str
    dose: str
    unit: str

    def __post_init__(self):
        self.dose: float = float(self.dose)
        self.patient_dose: Optional[float] = None

    def get_patient_dose(self, weight: int) -> float:
        self.patient_dose = float(weight) * self.dose
        return round(self.patient_dose, 1)


@dataclass
class DragInjection(BaseDrag):
    flask_dose: str
    flask_unit: str

    def __post_init__(self):
        super().__post_init__()
        self.flask_dose: float = float(self.flask_dose)

    @staticmethod
    def prepare_dose(dose):
        if dose > 10:
            return int(dose)
        else:
            return dose

    def get_patient_dose_in_flasks(self):
        return round(self.patient_dose / self.flask_dose, 1)

    def count(self, weight: int) -> dict:
        dose_per_kg = f'{self.prepare_dose(self.dose)}/кг'
        dose_in_str = f'{self.prepare_dose(self.get_patient_dose(weight))}{self.unit}'
        flasks = f'{self.get_patient_dose_in_flasks()} {self.flask_unit}'
        answer = {
            'препарат': self.drag, 'расчет': dose_per_kg, 'доза': dose_in_str, 'ед': flasks
        }
        return answer


coef_dict = {
    'mkg': 0.001
}


@dataclass
class DragInfusion(BaseDrag):
    concentration: str
    drag_id: str

    def __post_init__(self):
        super().__post_init__()
        self.dose_unit_in_mg: float = coef_dict[self.unit]
        self.concentration: float = float(self.concentration)

    def get_infusion_speed(self, weight, flasks, finish_volume=50):
        dose_per_h_in_mg = self.get_patient_dose(weight) * 60 * self.dose_unit_in_mg
        print(dose_per_h_in_mg)

        concentration_in_finish_volume = flasks * self.concentration / finish_volume
        print(concentration_in_finish_volume)

        speed = round(dose_per_h_in_mg / concentration_in_finish_volume, 1)
        return speed

    def get_optimal_flasks_num(self, weight, finish_vol):
        optimal_infusion_speed = Limits(4, 10)
        for flasks in range(1, 20):
            speed = self.get_infusion_speed(weight, flasks, finish_vol)
            if speed in optimal_infusion_speed:
                return f'{flasks} ml {self.drag} to {finish_vol} ml, {speed} ml/h'


@dataclass
class PerWeightCounter:
    func_id: str
    weight: int

    def load_frame(self) -> list[dict]:
        path = Path(__file__).parent / 'data' / 'drag_dosage.json'
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get(self.func_id, [])

    def __call__(self, *args, **kwargs) -> str:
        drag_list_data = self.load_frame()

        drag_list = [DragInjection(**drag_row).count(self.weight)
                     for drag_row in drag_list_data]

        my_table = get_my_table_string(
            fields=['препарат', 'расчет', 'доза', 'ед'],
            rows=drag_list,
            divider=' | '
        )
        return my_table


@dataclass
class PerWeighTimeCounter(PerWeightCounter):
    drag_id: str
    finish_volume: int

    def __call__(self, *args, **kwargs) -> str:
        drag_list_data = self.load_frame()

        drag_data = next(item for item in drag_list_data if item.get('drag_id') == self.drag_id)
        drag_inf = DragInfusion(**drag_data)
        return drag_inf.get_optimal_flasks_num(self.weight, self.finish_volume)


if __name__ == '__main__':
    # drag = BaseDrag('na', '10')
    # drag = DragInjection('nor', '10', 'mg', '500', 'fl')
    drag = DragInfusion('nor', '0.3', 'mkg', '2', 'n_id')
    report = drag.get_optimal_flasks_num(50, 50)
    func = PerWeighTimeCounter('per_hour_count', 70, 'd_na', 50)
    print(func())

