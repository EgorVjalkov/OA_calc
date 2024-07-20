from aiogram.filters.state import State, StatesGroup


class PatientDataInput(StatesGroup):
    func_menu = State()
    sma_confirm = State()
    apache_change = State()

    patient_parameters_menu = State()
    patient_parameters_menu_if_scrolling = State()

    value_input_by_kb = State()
    value_input_by_kb_if_scrolling = State()

    value_input_menu = State()
    value_input_menu_if_scrolling = State()

    report_menu = State()
    report_menu_if_scrolling = State()

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
