class BloodVolCounter:

    def __init__(self, height=0, weight=0, weight_before=0):
        self.height = height
        self.weight = weight
        self.weight_before_preg = weight_before
        self.blood_volume = 0

    @property
    def bmi(self):
        return round(self.weight/pow(self.height/100, 2), 1)

    @property
    def bmi_before_preg(self):
        return round(self.weight_before_preg / pow(self.height / 100, 2), 1)

    @property
    def get_blood_volume(self):
        if not self.blood_volume:
            if self.bmi_before_preg < 40:
                self.blood_volume = 100 * self.weight_before_preg
            else:
                self.blood_volume = 80 * self.weight_before_preg
        return self.blood_volume


class BleedCounter:
    def __init__(self, blood_vol: int):
        self.blood_vol = blood_vol

    def count_bleed_volume(self, percents: tuple):
        def get_bleed_vol(percent):
            return (percent / 100) * self.blood_vol

        vol_list = [str(get_bleed_vol(percent)) for percent in percents]
        return vol_list


data = {'weight': 56, 'height': 146, 'weight_before': 52}
a = BloodVolCounter(**data)
blood_v = a.get_blood_volume
b = BleedCounter(blood_v)
clin = b.count_bleed_volume((10, 15))
crit = b.count_bleed_volume((25, 30))
print(blood_v, clin, crit)
