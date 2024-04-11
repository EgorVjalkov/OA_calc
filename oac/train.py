from oac.program_logic.patient import Patient
from dataclasses import dataclass, fields
from collections import namedtuple

if __name__ == '__main__':
    patient = Patient()
    patient.func_id = 'bleed_%_count'
    patient.set_current_params()

    patient.params.parameter_id = 'fetus'
    patient.params.current.value = 'big_f'

    patient.params.parameter_id = 'weight'
    patient.params.current.value = 61

    patient.params.parameter_id = 'weight_before'
    patient.params.current.value = 55

    patient.params.parameter_id = 'height'
    patient.params.current.value = 167

    patient.params.parameter_id = 'bleed_vol'
    patient.params.current.value = 1670

    bnt = patient.params.get_btns()
    print(patient.params.current_params)
    patient.change_func()
    result = patient.get_result()
    rep = patient.get_reports(last=True)
    print(rep)
