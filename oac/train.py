from oac.program_logic.patient import Patient


if __name__ == '__main__':
    patient = Patient()
    patient.func_id = 'sma_count'
    patient.set_current_params()

    bnt = patient.params.get_btns()
    print(bnt)

    patient.params.parameter_id = 'fetus'

    fetus_btns = patient.params.current.get_btns()
    print(fetus_btns)

    patient.params.current.value = 'big_f'

    bnt = patient.params.get_btns()
    print(bnt)
