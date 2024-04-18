from aiogram.filters.state import State, StatesGroup


class PatientDataInput(StatesGroup):
    func_menu = State()
    sma_confirm = State()
    patient_parameters_menu = State()
    parameter_value_input = State()
    parameter_value_menu = State()
    print_report = State()
    finish_and_print = State()


class FeedBack(StatesGroup):
    ask_menu = State()


class Theory(StatesGroup):
    func_menu = State()
    theory = State()
