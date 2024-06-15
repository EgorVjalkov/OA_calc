from dataclasses import fields, field

from oac.program_logic.apacheII_counter import ApacheIICounterFio2Less50
from oac.program_logic.scale_counter import BaseScale
from oac.program_logic.patientparameter import Limits

scale = BaseScale()
print(scale)
scale.get_scale_frame('apacheII')
print(scale.data)
print(scale.lethality_frame)

apacheII = ApacheIICounterFio2Less50(
    56,
    37.0,
    40,
    110,
    28,
    56,
    7.02,
    135,
    4.5,
    320,
    0.45,
    22,
    15,
    'chronic',
    'emerg'
)


print(apacheII.get_apacheII_scores())
print(apacheII.total_score)
print(apacheII.get_lethality())
