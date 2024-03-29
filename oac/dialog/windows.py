from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Start, Cancel, Back, SwitchTo
from aiogram_dialog.widgets.input.text import TextInput

from oac.dialog.states import PatientDataInput
from oac.dialog import kbs
from oac.dialog import selected
from oac.dialog import getters
from oac.dialog.variants_with_id import sma_confirm_text


def greet_window() -> Window:
    return Window(
        Const('Привет, это бот для расчетов в акушерской анестезиологии. '
              'Что считаем?'),
        kbs.group_kb_for_func_menu(selected.on_chosen_func,
                             'func', 'funcs'),
        SwitchTo(Const('никаких задач'),
                 id='sw_finish',
                 state=PatientDataInput.print_finish_session_report),
        state=PatientDataInput.func_menu,
        getter=getters.get_funcs,
    )


def sma_confirm_window():
    return Window(
        Const(sma_confirm_text),
        SwitchTo(Const('Понимаю'),
                 id='sw_to_input',
                 state=PatientDataInput.patient_parameters_menu),
        state=PatientDataInput.sma_confirm
    )


def input_patient_data_window() -> Window:
    return Window(
        Format('{topic}'),
        kbs.group_kb_for_patient_params_menu(selected.on_chosen_patient_data,
                                             'pat_param', 'patient_parameters'),
        SwitchTo(Const('<< назад'),
                 id='sw_func_menu',
                 state=PatientDataInput.func_menu),
        state=PatientDataInput.patient_parameters_menu,
        getter=getters.get_data_for_pat_params_menu,
    )


def input_window() -> Window:
    return Window(
        Format('{topic}'),
        TextInput(id='enter_data',
                  on_success=selected.on_entered_parameter_value),
        SwitchTo(Const('<< назад'),
                 id='sw_to_in_menu',
                 state=PatientDataInput.patient_parameters_menu),
        state=PatientDataInput.parameter_value_input,
        getter=getters.get_topic_for_input,
    )


def select_window() -> Window:
    return Window(
        Format('{topic}'),
        kbs.group_kb_for_func_menu(selected.on_chosen_parameter_value, id_='ch_param', select_items='param_vars'),
        SwitchTo(Const('<< назад'),
                 id='sw_to_in_menu',
                 state=PatientDataInput.patient_parameters_menu),
        state=PatientDataInput.parameter_value_menu,
        getter=getters.get_kb_for_select_parameter,
    )


def report_window() -> Window:
    return Window(
        Format('{result}'),
        SwitchTo(Const('<< изменить параметры'),
                 id='sw_to_input_menu',
                 state=PatientDataInput.patient_parameters_menu),
        SwitchTo(Const('<< назад в меню функций'),
                 id='sw_to_func_menu',
                 state=PatientDataInput.func_menu),
        SwitchTo(Const('задача решена!'),
                 id='sw_to_finish_report',
                 state=PatientDataInput.print_finish_session_report),
        state=PatientDataInput.print_report,
        getter=getters.get_report)


def finish_window():
    return Window(
        Format("{result}"),
        Cancel(Const('до встречи!'),
               on_click=selected.on_adieu),
        state=PatientDataInput.print_finish_session_report,
        getter=getters.get_report,
    )


dialog = Dialog(greet_window(),
                sma_confirm_window(),
                input_patient_data_window(),
                select_window(),
                input_window(),
                report_window(),
                finish_window(),
                )
