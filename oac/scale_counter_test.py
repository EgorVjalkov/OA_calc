from oac.program_logic.scale_counter import SofaCounter, BaseScale
from oac.program_logic.patientparameter import Limits

scale = BaseScale()
print(scale)
scale.get_scale_frame('sofa')
print(scale.data)
print(scale.lethality_frame)

sofa = SofaCounter(
    0.21,
    40,
    'resp_support',
    110,
    35,
    2,
    14,
    100,
    1000,
)

rep = sofa()
print(rep)
