block_level_list = ['>=T4'] + list('T' + str(i) for i in range(5, 9)) + ['<=T10']
patient_file_questionnaire = {
    'position for puncture': ('lying', 'sitting'),
    'dose of 0.5% heavy bupivacaine, ml': 0,
    'dose of 0.005% fentanyl, if using, ml': 0,
    'puncture-delivering interval, min': 0,
    'sensory block level in 5 min': block_level_list,
    'events for raising/lowering block level': ('raising head of operating table', 'lowering head of operating table', 'no need'),
    'dose of 0.005% fenylefrine BEFORE delivering, ml': 0,
    'sensory block level AFTER delivering': block_level_list,
    'dose of 0.005% fenylefrine AFTER delivering, ml': 0,
    'expansion of the scope of surgery': ('опишите if True', 'False'),
    'complaints of pain during surgery': ('опишите if True', 'False'),
    'doctor`s estimation': tuple(str(i) for i in range(1, 6)),
    'patient`s estimation': tuple(str(i) for i in range(1, 6)),
    'remark': ''
}
