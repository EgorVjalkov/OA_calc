

class RiskFactor:
    def __init__(self, name, data):
        self.name = name
        self.risk_factor_dict = data[name]['risk_factor_dict']
        if 'description' in data[name]:
            self.description = data[name]['description']

        self.risk_factor_data = {'name': self.name}

    def get_bmi_risk_count(self,
                           bmi: float,
                           behavior: str = '') -> dict | int:

        for k in self.risk_factor_dict:
            if bmi < k:
                self.risk_factor_data['interpretation'] = self.risk_factor_dict[k]['inter']
                self.risk_factor_data['count'] = self.risk_factor_dict[k]['count']
                if behavior == 'blood_vol_count':
                    self.risk_factor_data['blood_vol_coef'] = self.risk_factor_dict[k]['blood_vol_coef']
                return self.risk_factor_data

    def find_risk_factor_with_answer(self,
                                     answer: str) -> dict:

        self.risk_factor_data['interpretation'] = self.risk_factor_dict[answer]['inter']
        self.risk_factor_data['count'] = self.risk_factor_dict[answer]['count']
        return self.risk_factor_data

    def input_risk_factor_and_get_count(self, tg_data):
        interpretation_list = {k: self.risk_factor_dict[k]['inter']
                               for k in self.risk_factor_dict}
        for k in self.risk_factor_dict:
            if tg_data in self.risk_factor_dict[k].values():
                self.risk_factor_data['count'] = self.risk_factor_dict[k]['count']
        return self.risk_factor_data


#a = RiskFactor('fetus', data.risk_factor_dict)
#a.input_risk_factor_and_get_count()
