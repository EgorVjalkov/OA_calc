from aiogram.filters.state import State, StatesGroup


class PatientDataInput(StatesGroup):
    func_menu = State()
    input_patient_data_menu = State()
    input_parameter = State()
    report = State()
    finish_session_report = State()
