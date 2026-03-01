from typing import Optional
from dataclasses import dataclass, InitVar

from oac.program_logic.data_loader import data_loader

from oac.program_logic.my_table import get_my_table_string
from oac.program_logic.patientparameter import Limits


@dataclass
class BaseDrug:
    drug: str
    dose: str
    unit: str

    def __post_init__(self):
        self.dose: float = float(self.dose)
        self.patient_dose: Optional[float] = None

    def get_patient_dose(self, weight: int) -> float:
        self.patient_dose = float(weight) * self.dose
        return round(self.patient_dose, 1)


@dataclass
class DrugInjection(BaseDrug):
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

    def count(self, weight: int) -> list:
        dose_per_kg = f'{self.prepare_dose(self.dose)}/кг'
        dose_in_str = f'{self.prepare_dose(self.get_patient_dose(weight))}{self.unit}'
        flasks = f'{self.get_patient_dose_in_flasks()} {self.flask_unit}'
        answer = [self.drug, dose_per_kg, dose_in_str, flasks]
        return answer


coef_dict = {
    'mkg': 0.001
}


@dataclass
class DrugInfusion(BaseDrug):
    concentration: str
    drug_id: str

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
                return f'{flasks} ml {self.drug} to {finish_vol} ml, {speed} ml/h'


@dataclass
class PerWeightCounter:
    func_id: str
    weight: int

    def load_frame(self) -> list[dict]:
        res = data_loader.drug_dosage_data.get(self.func_id, [])
        print(f"DEBUG load_frame: func_id='{self.func_id}', keys={list(data_loader.drug_dosage_data.keys())[:3]}")
        return res

    def calculate(self) -> str:
        drug_list_data = self.load_frame()

        drug_list = [DrugInjection(**drug_row).count(self.weight)
                     for drug_row in drug_list_data]

        my_table = get_my_table_string(
            fields=['препарат', 'расчет', 'доза', 'ед'],
            rows=drug_list,
            divider=' | '
        )
        return my_table


@dataclass
class PerWeighTimeCounter(PerWeightCounter):
    drug_id: str
    finish_volume: int

    def calculate(self) -> str:
        drug_list_data = self.load_frame()

        drug_data = next(item for item in drug_list_data if item.get('drug_id') == self.drug_id)
        drug_inf = DrugInfusion(**drug_data)
        return drug_inf.get_optimal_flasks_num(self.weight, self.finish_volume)


if __name__ == '__main__':
    # drug = BaseDrug('na', '10')
    # drug = DrugInjection('nor', '10', 'mg', '500', 'fl')
    drug = DrugInfusion('nor', '0.3', 'mkg', '2', 'n_id')
    report = drug.get_optimal_flasks_num(50, 50)
    func = PerWeighTimeCounter('per_hour_count', 70, 'd_na', 50)
    print(func.calculate())

