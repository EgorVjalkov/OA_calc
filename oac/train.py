from oac.program_logic.patient import Patient
from dataclasses import dataclass, fields
from collections import namedtuple

Limits = namedtuple('Limits', 'min max')
lims = '40 160'
limits = Limits(*lims.split())

if __name__ == '__main__':
    patient = Patient()
    patient.func_id = 'drag_count'
    patient.set_current_params()

    patient.params.parameter_id = 'fetus'
    patient.params.current.value = 'big_f'

    patient.params.parameter_id = 'weight'
    patient.params.current.value = 161

    patient.params.parameter_id = 'height'
    patient.params.current.value = 167

    bnt = patient.params.get_btns()
    patient.change_func()
    result = patient.get_result()
    rep = patient.get_reports(last=True)
    print(rep)
