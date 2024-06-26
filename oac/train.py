from oac.program_logic.patient import Patient
from dataclasses import dataclass, fields
from collections import namedtuple
from oac.program_logic.apacheII_counter import ApacheIICounterFio2Less50
from oac.program_logic.patientparameter import SelectedParameter
from fastnumbers import fast_real

test_params = (
    0.21,
    40,
    'nivl_resp',
    110,
    35,
    'mid_hp',
    14,
    210,
    500,
)

apache_test = (
    0.56, #fio2
    56,
    15,
    135.2,
    40,
    40.2,
    60,
    120,
    20,
    35, #paco2
    7.000,
    130.2,
    4,
    0.452,
    22,
    'chronic',
    'emerg',
)

patient = Patient()
#patient.func_id = 'apacheIIFio2less50_count'
patient.func_id = 'apacheII_count'
patient.params.set_current_params(patient.func_id)
print(patient.params.current_params)
g = (i for i in apache_test)
for p in patient.params.current_params:
    param = next(g)
    print(p, param)
    patient.params.parameter_id = p
    patient.params.current.value = param


print(patient.params.current_params)

patient.params.parameter_id = 'weight'
patient.params.current.value = 61

patient.params.parameter_id = 'weight_before'
patient.params.current.value = 55

patient.params.parameter_id = 'height'
patient.params.current.value = 167

patient.params.parameter_id = 'bleed_vol'
patient.params.current.value = 1670

patient.params.parameter_id = 'fetus'
patient.params.current.value = 'big_f'

patient.params.parameter_id = 'bladder'
patient.params.current.value = 'poly_b'


patient.change_func()
rep = patient.get_result()
print(rep)


#
#
# def gen():
#     for i in apache_test:
#         yield i
#
#
# gen = gen()
#
#
# if __name__ == '__main__':
#     patient = Patient()
#     patient.func_id = 'apacheIIFio2less50_count'
#     patient.set_current_params()
#     for i in patient.params.current_params:
#         patient.params.parameter_id = i
#         patient.params.current.value = next(gen)
#
#     apache = ApacheIICounterFio2Less50(**patient.params.get_values())
#     rep = apache()
#     print(rep)

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

value = ['0', '0.00', '56', 'sldkfjs']

for v in value:
    v = fast_real(v)
    print(v)
    if not v:
        print(v, 'ноль')
    else:
        print(v, 'неноль')
