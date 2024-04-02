funcs = [
    ('примерный ОЦК', 'blood_vol_count'),
    ('дозировка медикаментов', 'drag_count'),
    ('расчет анестеника для СМА', 'sma_count')
]

general_patient_data = [
    ('рост', 'height'),
    ('вес', 'weight'),
]

accessory_patient_data_for_bleed = [
    ('вес до беременности', 'weight_before')
]

accessory_patient_data_for_sma = [
    ('вес плодa (плодов)', 'fetus'),
    ('плодный пузырь', 'bladder'),
    ('дискомфорт в положении лежа на спине', 'discomfort')
]

bleed_vars = general_patient_data.copy()
bleed_vars.extend(accessory_patient_data_for_bleed)
sma_vars = general_patient_data.copy()
sma_vars.extend(accessory_patient_data_for_sma)

fetus_vars = [
    ('вес > 4кг', '> 4кг',  1),
    ('2.5кг < вес < 4кг', '2.5-4кг', 0),
    ('вес < 2.5кг', '> 2.5кг', -1)
]

variants = {
    'funcs': funcs,
    'blood_vol_count': bleed_vars,
    'drag_count': [('вес', 'weight')],
    'sma_count': sma_vars,
    'fetus': fetus_vars,
    # 'bladder': bladder_vars,
    # 'discomfort' discomfort_vars,
}

sma_confirm_text = '''Я могу посчитать дозу анестетика для СМА. 
Функция экспериментальная и требует доработки. 

Необходимо соблюдать ряд правил:
1) использовать официнальные тяжелые растворы,
2) убедиться, что опер. стол ровный,
3) предпочесть пункцию в положении сидя,
4) вводить расчетную дозу как можно медленнее (~2мл/мин)'''

topics = {
    'blood_vol_count': 'Я могу посчитать предполагаемый ОЦК пациентки. Введите показатели.',
    'drag_count': 'Я могу рассчитать дозы медикаментов по весу пациентки.',
    'sma_count': 'Введите данные. Обратите внимание, ряд показателей имеет значение по умолчанию',
}

select_variant = ''

answers = {
    'height': 'роста в см',
    'weight': 'веса в кг',
    'weight_before': 'веса до беременности (текущий вес минус прибавка) в кг',
}


def get_dict_with_variants(key: str) -> dict:
    return {key: variants[key]}
