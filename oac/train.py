from oac.program_logic.patient import Patient
from dataclasses import dataclass, fields
from collections import namedtuple
from oac.program_logic.apacheII_counter import ApacheIICounterFio2Less50
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

apache_test = (
    56,
    13,
    40,
    56,
    40.2,
    62,
    130,
    25,
    7.02,
    135,
    4.5,
    0.45,
    22,
    'CHP',
    'emerg_oper'
)


def gen():
    for i in apache_test:
        yield i


gen = gen()


if __name__ == '__main__':
    patient = Patient()
    patient.func_id = 'apacheIIFio2less50_count'
    patient.set_current_params()
    for i in patient.params.current_params:
        patient.params.parameter_id = i
        patient.params.current.value = next(gen)

    apache = ApacheIICounterFio2Less50(**patient.params.get_values())
    rep = apache()
    #print(rep)

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
