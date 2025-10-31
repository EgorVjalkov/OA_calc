from oac.program_logic.patient import Patient


def sma_count(weight, height, fetus='normal_f', bladder='normal_b', discomfort='no_discomfort'):
    patient = Patient()
    patient.func_id = 'sma_count'

    patient.params.set_current_params(patient.func_id)

    patient.params.parameter_id = 'weight'
    patient.params.current.value = weight

    patient.params.parameter_id = 'height'
    patient.params.current.value = height

    patient.params.parameter_id = 'fetus'
    patient.params.current.value = fetus

    patient.params.parameter_id = 'bladder'
    patient.params.current.value = bladder

    patient.params.parameter_id = 'discomfort'
    patient.params.current.value = discomfort


    patient.change_func()
    rep = patient.get_result()
    print(rep)


if __name__ == '__main__':
    sma_count(
        weight=76,
        height=172,
        fetus='normal_f', #small_f, big_f
        bladder='normal_b', # poly_b
        discomfort='no_discomfort' # discomfort
    )

