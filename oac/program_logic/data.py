risk_factor_dict = {
    'bmi': {
        'risk_factor_dict': {
            18.5: {'inter': 'дефицит', 'count': -1, 'blood_vol_coef': 100},
            25.0: {'inter': 'норма', 'count': -1, 'blood_vol_coef': 100},
            30.0: {'inter': 'избыток', 'count': 0, 'blood_vol_coef': 100},
            35.0: {'inter': 'ожирение 1', 'count': 1, 'blood_vol_coef': 100},
            40.0: {'inter': 'ожирение 2', 'count': 2, 'blood_vol_coef': 85},
            100.0: {'inter': 'ожирение 3', 'count': 3, 'blood_vol_coef': 85}}},

    'fetus': {
        'risk_factor_dict': {
            'b': {'inter': 'крупный (вес > 4кг)', 'count': 1},
            'n': {'inter': 'normal (fetus weight > 2.5kg and < 4kg)', 'count': 0},
            's': {'inter': 'small (fetus weight < 2.5kg)', 'count': -1}},
        'description': 'fetus is'},

    'bladder': {
        'risk_factor_dict': {
            'r': {'inter': 'raptured or oligohydramnios', 'count': -1},
            'n': {'inter': 'intact, no polyhydramnios', 'count': 0},
            'p': {'inter': 'intact, polyhydramnios', 'count': 1}},
        'description': 'bladder is'},

    'back_discomfort': {
        'risk_factor_dict': {
            'y': {'inter': 'discomfort in the position on the back', 'count': 1},
            'n': {'inter': 'NOT discomfort in the position on the back', 'count': 0}},
        'description': 'pregnant has'}
}

translation_dict = {'рост': 'height', 'вес': 'weight', 'ИМТ': 'bmi',
            'по плоду': 'fetus', 'по объему аниотической жидкости': 'bladder', 'по дискомфорту в положении на спине': 'back_discomfort',
            'ОЦК': 'blood_vol', 'потеря 10-15% ОЦК': 'clinical_bleed', 'потеря 25-30% ОЦК': 'critical_bleed'}

blood_vol_menu = {
    'вес до беременности': 'answer2',
    'прибавку во время беременности': 'self.weight - answer2',
    'нет необходимости в подсчете ОЦК': '0'}

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

block_level_list = ['>=T4'] + list('T' + str(i) for i in range(5, 9)) + ['<=T10']
patient_file_questionnaire = {
    'position for puncture': ('lying', 'sitting'),
    'dose of 0.5% heavy bupivacaine, ml': 0,
    'dose of 0.005% fentanyl, if using, ml': 0,
    'puncture-delivering interval, min': 0,
    'sensory block level in 5 min': block_level_list,
    'events for raising/lowering block level': ('raising head of operating table', 'lowering head of operating table', 'no need'),
    'dose of 0.005% fenylefrine BEFORE delivering, ml': 0,
    'sensory block level AFTER delivering': block_level_list,
    'dose of 0.005% fenylefrine AFTER delivering, ml': 0,
    'expansion of the scope of surgery': ('опишите if True', 'False'),
    'complaints of pain during surgery': ('опишите if True', 'False'),
    'doctor`s estimation': tuple(str(i) for i in range(1, 6)),
    'patient`s estimation': tuple(str(i) for i in range(1, 6)),
    'remark': ''
}
