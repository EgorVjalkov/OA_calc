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
    210,
    1000,
)

ox = sofa.get_oxygenation_count()
print(sofa.oxygenation_index)
print(ox)
