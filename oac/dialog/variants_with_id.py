funcs = [
    ('спинальная анестезия', 'sma_count'),
    ('острая кровопотеря', 'blood_vol_count')
]

general_patient_data = [
    ('рост', 'height'),
    ('вес', 'weight'),
]

accessory_patient_data_for_bleed = [
    ('вес до беременности', 'weight_before')
]

accessory_patient_data_for_sma = [
    ('плод', 'fetus'),
    ('плодный пузырь', 'bladder'),
    ('дискомфорт в положении лежа на спине', 'discomfort')
]

bleed_vars = general_patient_data.copy()
bleed_vars.extend(accessory_patient_data_for_bleed)
sma_vars = general_patient_data.copy()
sma_vars.extend(accessory_patient_data_for_sma)

variants = {
    'funcs': funcs,
    'blood_vol_count': bleed_vars,
    'sma_count': sma_vars,
}

answers = {
    'height': 'роста в см',
    'weight': 'веса в кг',
    'weight_before': 'веса до беременности (текущий вес минус прибавка) в кг'
}


def get_dict_with_variants(key: str) -> dict:
    return {key: variants[key]}
