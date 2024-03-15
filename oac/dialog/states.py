from aiogram.filters.state import State, StatesGroup


class PatientDataInput(StatesGroup):
    func_menu = State()
    input_patient_data_menu = State()
    input_parameter = State()
    report = State()

    input_name = State()
    input_height = State()
    input_weight = State()

    input_puncture_position = State()
