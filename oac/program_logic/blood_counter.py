from dataclasses import dataclass


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
        if self.bmi_before_preg < 40:
            blood_volume = 100 * self.weight_before
        else:
            blood_volume = 80 * self.weight_before
        return blood_volume

    def count_bleed_volume(self, percents: tuple):
        def get_bleed_vol(percent):
            return int((percent / 100) * self.blood_volume)

        vol_list = [str(get_bleed_vol(percent)) for percent in percents]
        return vol_list

    def __call__(self, *args, **kwargs):
        clin_ = '-'.join(self.count_bleed_volume((10, 15)))
        crit_ = '-'.join(self.count_bleed_volume((25, 30)))
        return [
            f'Oбъем ОЦК ~ {self.blood_volume}мл',
            f'шок I ~ {clin_}мл',
            f'шок II-III ~ {crit_}мл',
        ]


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
    print(a.bmi)
