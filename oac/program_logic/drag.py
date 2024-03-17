from typing import Optional
import pandas as pd


class Drag:
    def __init__(self,
                 drag: str,
                 dose_per_kg: str,
                 unit: str,
                 flask_dose: str,
                 flask_unit: str):
        self.drag = drag
        self.dose_per_kg = float(dose_per_kg)
        self.unit = unit
        self.flask_dose = float(flask_dose)
        self.flask_unit = flask_unit

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
            f'вес: {weight} кг': self.drag, 'расчет': dose_per_kg, 'доза': dose_in_str, 'ед': flasks})
        return answer


def get_drag_list_answer(path: str, weight: int) -> str:
    drag_frame = pd.read_excel(path, dtype=str)

    drag_list = [Drag(*drag_frame.loc[i]).count(weight)
                 for i in drag_frame.index]
    answer_list = [' | '.join([f'вес: {weight}', 'расчет', 'доза', 'ед'])]
    for d in drag_list:
        d = ' | '.join(d)
        answer_list.append(d)

    answer = '\n'.join(answer_list)

    #drag_frame = pd.concat(drag_list, axis=1).T
    #drag_frame = drag_frame.set_index(drag_frame.columns[0])

    return answer


if __name__ == '__main__':
    path = 'drag_dosage.xlsx'
    frame = get_drag_list_answer(path, 85)
    print(frame)
