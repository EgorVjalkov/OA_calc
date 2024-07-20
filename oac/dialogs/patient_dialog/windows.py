from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Cancel, SwitchTo
from aiogram_dialog.widgets.input.text import TextInput

from oac.dialogs.states import PatientDataInput
from oac.dialogs.patient_dialog import getters, kbs, selected
from oac.dialogs.variants_with_id import sma_confirm_text, apache_text

from oac.dialogs.patient_dialog.my_windows import ReportWindow, ParamsWindow, ParamOnClickInputWindow, ParamKbInputWindow


def greet_window() -> Window:
    return Window(
        Const('Выберите функцию для расчетов'),
        kbs.Keyboard('simple_by_item', 'func', 'funcs'
                     ).get_kb(selected.on_chosen_func),
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


def apache_change_window() -> Window:
    return Window(
        Const(apache_text),
        kbs.Keyboard('simple_by_item', 'apache', 'apaches'
                     ).get_kb(selected.on_chosen_apache_scale),
        SwitchTo(Const('<< назад'),
                 id='sw_func_menu',
                 state=PatientDataInput.func_menu),
        state=PatientDataInput.apache_change,
        getter=getters.get_apaches,
    )


def params_menu_if_simple() -> ParamsWindow:
    return ParamsWindow(
        keyboard=kbs.Keyboard('simple_by_attr', 'params', 'patient_parameters'
                              ).get_kb(selected.on_chosen_patient_parameter),
        state=PatientDataInput.patient_parameters_menu,
    )


def params_menu_if_scrolling() -> Window:
    return ParamsWindow(
        keyboard=kbs.Keyboard('scroll_by_attr', 'params', 'patient_parameters'
                              ).get_kb(selected.on_chosen_patient_parameter),
        state=PatientDataInput.patient_parameters_menu_if_scrolling,
    )


def input_menu_if_simple() -> Window:
    return ParamKbInputWindow(
        state=PatientDataInput.value_input_by_kb,
        state_for_change_params=PatientDataInput.patient_parameters_menu)


def input_menu_if_scrolling() -> Window:
    return ParamKbInputWindow(
        state=PatientDataInput.value_input_by_kb_if_scrolling,
        state_for_change_params=PatientDataInput.patient_parameters_menu_if_scrolling)


def change_param_value_menu_if_simple() -> Window:
    return ParamOnClickInputWindow(
        state=PatientDataInput.value_input_menu,
        state_for_change_params=PatientDataInput.patient_parameters_menu)


def change_param_value_menu_if_scrolling() -> Window:
    return ParamOnClickInputWindow(
        state=PatientDataInput.value_input_menu_if_scrolling,
        state_for_change_params=PatientDataInput.patient_parameters_menu_if_scrolling)


def report_window_if_simple() -> ReportWindow:
    return ReportWindow(
        state=PatientDataInput.report_menu,
        state_for_change_params=PatientDataInput.patient_parameters_menu
    )


def report_window_if_scrolling() -> ReportWindow:
    return ReportWindow(
        state=PatientDataInput.report_menu_if_scrolling,
        state_for_change_params=PatientDataInput.patient_parameters_menu_if_scrolling
    )


def finish_window():
    return Window(
        Format("{result}"),
        Cancel(Const('до встречи!'),
               on_click=selected.on_adieu),
        state=PatientDataInput.print_finish_session_report,
        getter=getters.get_report,
    )


patient_dialog = Dialog(greet_window(),
                        sma_confirm_window(),
                        apache_change_window(),
                        params_menu_if_simple(),
                        params_menu_if_scrolling(),
                        change_param_value_menu_if_simple(),
                        change_param_value_menu_if_scrolling(),
                        input_menu_if_simple(),
                        input_menu_if_scrolling(),
                        report_window_if_simple(),
                        report_window_if_scrolling(),
                        finish_window(),
                        )
