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
        Const('Привет, я - бот для расчетов в акушерской анестезиологии. '
              'Что считаем?'),
        kbs.group_kb_by_item(selected.on_chosen_func,
                             'func', 'funcs'),
        SwitchTo(Format('{finish}'),
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


def select_patient_patameter_menu() -> Window:
    return Window(
        Format('{topic}'),
        kbs.group_kb_by_attr(selected.on_chosen_patient_parameter,
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


def change_param_value_menu() -> Window:
    return Window(
        Format('{topic}'),
        kbs.group_kb_by_attr(selected.on_chosen_parameter_value,
                             id_='ch_param', select_items='param_values'),
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
                select_patient_patameter_menu(),
                change_param_value_menu(),
                input_window(),
                report_window(),
                finish_window(),
                )
