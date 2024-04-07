from dataclasses import dataclass

from oac.program_logic.my_table import get_my_table_string


@dataclass
class BloodVolCounter:
    height: int
    weight: int
    weight_before: int

    def __post_init__(self):
        self.bmi = round(self.weight / pow(self.height / 100, 2), 1)
        self.bmi_before_preg = round(self.weight_before / pow(self.height / 100, 2), 1)

    @property
    def blood_volume(self):
        weight_for_calc = min((self.weight, self.weight_before))
        if self.bmi_before_preg < 40:
            blood_volume = 100 * weight_for_calc
        else:
            blood_volume = 80 * weight_for_calc
        return blood_volume

    def count_bleed_volume(self, percents: tuple):
        def get_bleed_vol(percent):
            return int((percent / 100) * self.blood_volume)

        vol_list = [str(get_bleed_vol(percent)) for percent in percents]
        return vol_list

    def __call__(self, *args, **kwargs):
        clin_ = '-'.join(self.count_bleed_volume((10, 15)))
        crit_ = '-'.join(self.count_bleed_volume((25, 30)))
        rows = [
            ['Oбъем ОЦК', f'~ {self.blood_volume}мл'],
            ['шок I', f'~ {clin_}мл'],
            ['шок II-III', f'~ {crit_}мл'],
        ]
        return get_my_table_string(fields=[], rows=rows, header=False)


class BleedCounter:
    def __init__(self, blood_vol: int):
        self.blood_vol = blood_vol

    def count_bleed_volume(self, percents: tuple):
        def get_bleed_vol(percent):
            return int((percent / 100) * self.blood_vol)

        vol_list = [str(get_bleed_vol(percent)) for percent in percents]
        return vol_list


if __name__ == '__main__':
    data = {'weight': 56, 'height': 146, 'weight_before': 52}
    a = BloodVolCounter(**data)
    rep = a()
    print(rep)
