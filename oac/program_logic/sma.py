from dataclasses import dataclass


@dataclass
class SmaCounter:
    height: int
    weight: int
    fetus: int
    bladder: int
    discomfort: int

    def get_bmi(self, weight):
        self.bmi = round(weight / pow(self.height / 100, 2), 1)
        return self.bmi


# counting sum of factors
def count_risk_factors(self, answers=()):
    for rf in self.risk_factors:
        rf = RiskFactor(rf, risk_factor_dict)
        if rf.name == 'bmi':
            rf_dict = rf.get_bmi_risk_count(self.bmi)
            print(f'ИМТ - {self.bmi}, ({rf_dict["interpretation"]})')

        else:
            if rf.name in answers and answers[rf.name]:
                rf_dict = rf.find_risk_factor_with_answer(answers[rf.name])
            else:
                rf_dict = rf.input_risk_factor_and_get_count()

        print(f'{rf.name} riskfactor is {rf_dict["count"]}', '\n')
        self.factors_count_dict.update({rf.name: rf_dict['count']})
        self.patient_data_for_spinal.update(
            {f'{rf.name}_{k}': rf_dict[k] for k in rf_dict if k in ['interpretation', 'count']})

    return self.risk_factors


def count_a_sum(self):
    back_discomfort_count = self.factors_count_dict.pop('back_discomfort')
    self.sum_of_factors = sum(list(self.factors_count_dict.values()))
    # присмотрись протестируй
    if self.sum_of_factors <= 0 and back_discomfort_count:
        self.sum_of_factors += back_discomfort_count
    elif self.sum_of_factors > 0 and back_discomfort_count:
        self.patient_data_for_spinal['back_discomfort_count'] = 'not using'
        print('данные о дискомфорте в положении на спине не использованы')

    self.patient_data_for_spinal['sum'] = self.sum_of_factors
    self.patient_data_for_spinal['limiting sum'] = False

    if self.sum_of_factors >= 4:
        self.sum_of_factors = 4
        self.patient_data_for_spinal['limiting sum'] = 4

    print(f'сумма факторов риска - {self.sum_of_factors}', '\n')
    return self.sum_of_factors


def get_bupivacaine_dose(self, sum_of_risk, bupivacaine_dosage):
    if self.height not in bupivacaine_dosage.keys():
        if self.height < 145:
            rounded_height = 145
        elif self.height > 180:
            rounded_height = 180
        else:
            rounded_height = self.height
            while rounded_height % 5 > 0:
                rounded_height += 1
    else:
        rounded_height = self.height

    counted_dose = bupivacaine_dosage[rounded_height][sum_of_risk + 2]
    counted_dose_for_sitting = round(counted_dose + 0.4, 1)
    self.patient_data_for_spinal['counted dose'] = counted_dose
    self.patient_data_for_spinal['counted dose for sitting'] = counted_dose_for_sitting
    print(f'0,5% доза тяжелого бупивакаина в положении лежа {counted_dose}ml\n')
    print(f'0,5% доза тяжелого бупивакаина в положении сидя {counted_dose_for_sitting}ml\n')

    return counted_dose
