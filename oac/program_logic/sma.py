from dataclasses import dataclass
from oac.program_logic.my_table import get_my_table_string

bmi_dict = {
        18.5: {'inter': 'дефицит', 'count': -1, 'blood_vol_coef': 100},
        25.0: {'inter': 'норма', 'count': -1, 'blood_vol_coef': 100},
        30.0: {'inter': 'избыток', 'count': 0, 'blood_vol_coef': 100},
        35.0: {'inter': 'ожирение 1', 'count': 1, 'blood_vol_coef': 100},
        40.0: {'inter': 'ожирение 2', 'count': 2, 'blood_vol_coef': 85},
        100.0: {'inter': 'ожирение 3', 'count': 3, 'blood_vol_coef': 85}
}

bupivacaine_dosage = {
    145: [1.5, 1.4, 1.4, 1.3, 1.2, 1.1, 1.0],
    150: [1.9, 1.8, 1.7, 1.5, 1.4, 1.4, 1.3],
    155: [2.1, 2.0, 1.8, 1.7, 1.6, 1.5, 1.4],
    160: [2.3, 2.2, 2.0, 1.9, 1.8, 1.6, 1.5],
    165: [2.4, 2.3, 2.2, 2.0, 1.9, 1.7, 1.6],
    170: [2.6, 2.4, 2.3, 2.1, 2.0, 1.8, 1.6],
    175: [2.8, 2.6, 2.4, 2.3, 2.1, 1.9, 1.8],
    180: [2.9, 2.8, 2.5, 2.4, 2.2, 2.0, 1.9]
}


@dataclass
class SmaCounter:
    weight: int
    height: int
    fetus_count: int
    bladder_count: int
    discomfort_count: int

    def __post_init__(self):
        bmi = round(self.weight / pow(self.height / 100, 2), 1)
        for i in bmi_dict.keys():
            if bmi < i:
                self.bmi_count = bmi_dict[i]['count']
                break

    def count_a_sum(self) -> int:
        sum_of_factors = sum((self.bmi_count, self.fetus_count, self.bladder_count))

        if sum_of_factors <= 0 and self.discomfort_count:
            sum_of_factors += self.discomfort_count

        if sum_of_factors >= 4:
            sum_of_factors = 4

        return sum_of_factors

    def get_anesthetic_dose(self, sum_of_risk) -> float:
        match self.height:
            case h if h < 145:
                h = 145
            case h if h > 180:
                h = 180
            case h:
                for i in bupivacaine_dosage.keys():
                    if h < i:
                        h = i
                        break

        return bupivacaine_dosage[h][sum_of_risk+2]

    def __call__(self, *args, **kwargs) -> str:
        dose_for_lying = self.get_anesthetic_dose(self.count_a_sum())
        hyperbaric = round(dose_for_lying+0.4, 1)
        isobaric = round(dose_for_lying+1.2, 1)
        rows = [
            ['тип анестетика', 'доза в мл'],
            ['гипербарический', f'{hyperbaric}мл'],
            ['изобарический', f'{isobaric}мл'],
        ]
        return get_my_table_string(fields=[], rows=rows, header=False)


if __name__ == '__main__':
    sma = SmaCounter(60, 167, 0, -1, 1)
    print(sma())

