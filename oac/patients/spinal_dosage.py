from oac.program_logic import data
from oac.patients.data import risk_factor_dict
from oac.patients.RiskFactor import RiskFactor
from datetime import datetime


class Patient:

    def __init__(self, patient_name='noname', height=0, weight=0, weight_before=0):
        dt = datetime.today()
        self.datetime = dt.strftime('%d.%m.%Y %H:%M')
        self.patient_name = patient_name
        self.height = height
        self.weight = weight
        self.weight_before_pregnancy = weight_before
        self.bmi = 0.0

        self.blood_volume = 0
        self.clinical_bleed = 0
        self.critical_bleed = 0
        self.bleed_volume = 0
        self.bleed_percent = 0

        self.risk_factors = ('bmi', 'fetus', 'bladder', 'back_discomfort')
        self.factors_count_dict = {}
        self.sum_of_factors = 0

        self.patient_dict = {
            'datetime': self.datetime,
            'name': self.patient_name,
            'height': self.height,
            'weight': self.weight,
            'weight bofore pregnancy': self.weight_before_pregnancy
        }

        self.patient_data_for_spinal = {}
        self.patient_data_for_bleeding = {}

    # сделай мини фyнкцию чтоб обновлять словари

    def __repr__(self):
        return f'Patient: {self.patient_data_for_bleeding}'

    def refresh_data_dicts(self, key, value, data_dict='all'):
        if data_dict == 'spinal':
            self.patient_data_for_spinal[key] = value
        elif data_dict == 'bleeding':
            self.patient_data_for_bleeding[key] = value
        elif data_dict == 'all':
            self.patient_data_for_spinal[key] = value
            self.patient_data_for_bleeding[key] = value

    def input_a_bleed_vol(self):
        if self.bleed_volume:
            self.bleed_percent = int((self.bleed_volume / self.blood_volume) * 100)
            self.refresh_data_dicts('bleed_vol', self.bleed_volume, data_dict='bleeding')
            self.refresh_data_dicts('bleed_percent', self.bleed_percent, data_dict='bleeding')
            return self.bleed_volume, self.bleed_percent
        else:
            #    self.refresh_data_dicts('bleed_vol', 'неизвестно', data_dict='bleeding')
            return False

    # bmi
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

    def count_blood_volume(self) -> object:
        bmi_before_pregnancy = self.get_bmi(weight=self.weight_before_pregnancy)
        bmi_rf = RiskFactor('bmi', data.risk_factor_dict)
        bmi_rf.get_bmi_risk_count(bmi_before_pregnancy, 'blood_vol_count')
        blood_vol_coef = bmi_rf.risk_factor_data['blood_vol_coef']
        self.blood_volume = blood_vol_coef * self.weight_before_pregnancy
        return self.blood_volume

    def count_bleed_volume(self, percents=()):
        def get_bleed_vol(percent):
            return (percent / 100) * self.blood_volume

        vol_list = [str(get_bleed_vol(percent)) for percent in percents]
        return vol_list

    def count_patient_data(self, behavior='') -> object:
        if not self.bmi:
            self.bmi = self.get_bmi(self.weight)
            self.patient_dict['bmi'] = self.bmi

        if not self.blood_volume:
            self.blood_volume = self.count_blood_volume()
            if self.blood_volume:
                self.refresh_data_dicts('объем ОЦК', self.blood_volume, 'bleeding')
                self.clinical_bleed = f"{'-'.join(self.count_bleed_volume((10, 15)))}"
                self.refresh_data_dicts('клинически значимая кровопотреря', self.clinical_bleed, 'bleeding')
                self.critical_bleed = f"{'-'.join(self.count_bleed_volume((25, 30)))}"
                self.refresh_data_dicts('массивная кровопотеря', self.critical_bleed, 'bleeding')

        return self

    def get_report(self, behavior: str) -> str:
        answer_list = []
        if behavior == 'blood_vol_count':
            for i in self.patient_data_for_bleeding:
                answer_list.append(f'{i} ~ {self.patient_data_for_bleeding[i]}')
        return '\n'.join(answer_list)


if __name__ == '__main__':

    pat = Patient(height=160, weight=110, weight_before=100)
    pat.count_patient_data('blood_vol_count')
    print(pat)
    print(pat.bmi)
    rep = pat.get_report('blood_vol_count')
    print(rep)
