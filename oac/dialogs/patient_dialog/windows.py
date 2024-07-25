from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Cancel, SwitchTo
from aiogram_dialog.widgets.input.text import TextInput

from oac.dialogs.states import PatientSession
from oac.dialogs.patient_dialog import getters, selected
from oac.dialogs.variants_with_id import sma_confirm_text, apache_text

from oac.dialogs.patient_dialog.my_wins_kbs_btns import ParamsWindow, MyBackButton, Keyboard


def greet_window() -> Window:
    return Window(
        Const('Выберите функцию для расчетов'),
        Keyboard('simple_by_item', 'func', 'funcs'
                 ).get_kb(selected.on_chosen_func),
        SwitchTo(Format('{finish}'),
                 id='sw_finish',
                 state=PatientSession.print_finish_session_report),
        state=PatientSession.func_menu,
        getter=getters.get_funcs,
    )


def sma_confirm_window():
    return Window(
        Const(sma_confirm_text),
        SwitchTo(Const('Понимаю'),
                 id='sw_to_input',
                 state=PatientSession.patient_parameters_menu),
        state=PatientSession.sma_confirm
    )


def apache_change_window() -> Window:
    return Window(
        Const(apache_text),
        Keyboard('simple_by_item', 'apache', 'apaches'
                 ).get_kb(selected.on_chosen_apache_scale),
        SwitchTo(Const('<< назад'),
                 id='sw_func_menu',
                 state=PatientSession.func_menu),
        state=PatientSession.apache_change,
        getter=getters.get_apaches,
    )


def params_menu_if_simple() -> ParamsWindow:
    return ParamsWindow(
        keyboard=Keyboard('simple_by_attr', 'params', 'patient_parameters'
                          ).get_kb(selected.on_chosen_patient_parameter),
        state=PatientSession.patient_parameters_menu,
    )


def params_menu_if_scrolling() -> Window:
    return ParamsWindow(
        keyboard=Keyboard('scroll_by_attr', 'params', 'patient_parameters'
                          ).get_kb(selected.on_chosen_patient_parameter),
        state=PatientSession.patient_parameters_menu_if_scrolling,
    )


def param_value_textinput_menu() -> Window:
    return Window(
        Format('{topic}'),
        TextInput(id='enter_data',
                  on_success=selected.on_entered_parameter_value),
        MyBackButton(selected.on_back_to_params_menu),
        state=PatientSession.value_textinput,
        getter=getters.get_topic_for_input,
    )


def param_value_onclickinput_menu() -> Window:
    return Window(
        Format('{topic}'),
        Keyboard('simple_by_attr', 'value', 'param_values'
                 ).get_kb(selected.on_chosen_parameter_value),
        MyBackButton(selected.on_back_to_params_menu),
        state=PatientSession.value_onclickinput,
        getter=getters.get_data_for_onclickinput,
    )


def report_menu() -> Window:
    return Window(
        Format('{result}'),
        # Const('результат в закрепленном сообщении'),
        MyBackButton(on_click=selected.on_back_to_params_menu,
                     text='<< изменить параметры'),
        SwitchTo(Const('<< назад в меню функций'),
                 id='sw_to_func_menu',
                 state=PatientSession.func_menu),
        # on_click=selected.on_send_report_msg), # закреп себя не оправдал. быть может нужно через другого бота...
        SwitchTo(Const('задача решена!'),
                 id='sw_to_finish_report',
                 state=PatientSession.print_finish_session_report),
        state=PatientSession.report_menu,
        getter=getters.get_report
    )


def finish_window():
    return Window(
        Format("{result}"),
        Cancel(Const('до встречи!'),
               on_click=selected.on_adieu),
        state=PatientSession.print_finish_session_report,
        getter=getters.get_report,
    )


patient_dialog = Dialog(greet_window(),
                        sma_confirm_window(),
                        apache_change_window(),
                        params_menu_if_simple(),
                        params_menu_if_scrolling(),
                        param_value_textinput_menu(),
                        param_value_onclickinput_menu(),
                        report_menu(),
                        finish_window(),
                        )
