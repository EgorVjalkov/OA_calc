from Menu import Menu


class Patient:

    def __init__(self, patient_name='noname', height=0, weight=0):
        self.patient_name = patient_name
        self.height = height
        self.weight = weight
        self.weight_before_preg = 0
        self.blood_volume = 0

    @property
    def set_height(self):
        if not self.height:
            menu = Menu(topic='Введите показатель роста в сантиметрах', variants=0)
            menu.print_a_topic()
            self.height = menu.get_user_answer()
        return self.height

    @property
    def set_weight(self):
        if not self.weight:
            menu = Menu(topic='Введите показатель веса в килограммах', variants=0)
            menu.print_a_topic()
            self.weight = menu.get_user_answer()
        return self.weight

    @property
    def set_weight_before_preg(self):
        if not self.weight_before_preg:
            menu = Menu(topic='Введите показатель веса до беременности в килограммах', variants=0)
            menu.print_a_topic()
            self.weight_before_preg = menu.get_user_answer()
        return self.weight_before_preg

    @property
    def bmi(self):
        return round(self.set_weight/pow(self.set_height/100, 2), 1)

    @property
    def bmi_before_preg(self):
        return round(self.set_weight_before_preg / pow(self.set_height / 100, 2), 1)

    @property
    def set_blood_volume(self):
        if not self.blood_volume:
            if self.bmi_before_preg < 40:
                self.blood_volume = 100 * self.set_weight_before_preg
            else:
                self.blood_volume = 80 * self.set_weight_before_preg
        return self.blood_volume


a = Patient()
print(a.set_blood_volume)
