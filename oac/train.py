from oac.program_logic.patient import Patient
from dataclasses import dataclass, fields
from collections import namedtuple
from oac.program_logic.scale_counter import SofaCounter
test_params = (
    0.21,
    40,
    'ivl_resp',
    110,
    35,
    'mid_hp',
    14,
    210,
    1000,
)


def gen():
    for i in test_params:
        yield i


gen = gen()


if __name__ == '__main__':
    patient = Patient()
    patient.func_id = 'sofa_count'
    patient.set_current_params()
    for i in patient.params.current_params:
        patient.params.parameter_id = i
        patient.params.current.value = next(gen)

    print(patient.params.get_btns())

    sofa = SofaCounter(**patient.params.get_values())
    rep = sofa()
    print(rep)

#    patient.params.parameter_id = 'weight'
#    patient.params.current.value = 61
#
#    patient.params.parameter_id = 'weight_before'
#    patient.params.current.value = 55
#
#    patient.params.parameter_id = 'height'
#    patient.params.current.value = 167
#
#    patient.params.parameter_id = 'bleed_vol'
#    patient.params.current.value = 1670
#
#    bnt = patient.params.get_btns()
#    print(patient.params.current_params)
#    patient.change_func()
#    result = patient.get_result()
#    rep = patient.get_reports(last=True)
#    print(rep)
