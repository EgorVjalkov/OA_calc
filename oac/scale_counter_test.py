from oac.program_logic.scale_counter import SofaCounter


sofa = SofaCounter(
    0.3,
    65,
    'support',
    110,
    35,
    2,
    14,
    210,
    1000,
)

sofa.get_oxygenation_count()
