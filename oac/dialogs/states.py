from aiogram.filters.state import State, StatesGroup


class PatientDataInput(StatesGroup):
    func_menu = State()
    sma_confirm = State()
    patient_parameters_menu = State()
    parameter_value_input = State()
    parameter_value_menu = State()
    report_menu = State()
    print_finish_session_report = State()


class FeedBack(StatesGroup):
    ask_menu = State()


class Theory(StatesGroup):
    theory = State()


class KES(StatesGroup):
    menu = State()
    calculator = State()
    parameter_value_input = State()
    report_menu = State()
    reference = State()
