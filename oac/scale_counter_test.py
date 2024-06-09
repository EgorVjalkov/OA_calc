from oac.program_logic.scale_counter import SofaCounter
from oac.program_logic.patientparameter import Limits


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
