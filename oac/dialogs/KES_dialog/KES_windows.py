from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Cancel, SwitchTo
from aiogram_dialog.widgets.input.text import TextInput

from oac.dialogs.patient_dialog.selected import on_adieu
from oac.dialogs.patient_dialog.my_wins_kbs_btns import Keyboard
from oac.dialogs.states import KES
from oac.dialogs.KES_dialog import KES_getters, KES_selected


def KES_menu_window() -> Window:
    return Window(
        Const('Могу помочь в рассчетах для КЭС'),
        SwitchTo(Const('расчет времени пребывания'),
                 id='sw_time',
                 state=KES.calculator),
        # SwitchTo(Const('справка по КЭСам'),
        #          id='sw_ref',
        #          state=KES.reference),
        Cancel(Const('спасибо, не надо'),
               on_click=on_adieu),
        state=KES.menu
    )


def time_calculator_menu() -> Window:
    return Window(
        Const('Выберите пункт меню'),
        Keyboard('simple_by_attr', 's_time', 'time_for_KES'
                 ).get_kb(KES_selected.on_chosen_kes_parameter),
        SwitchTo(Const('<< назад'),
                 id='sw_KES_menu',
                 state=KES.menu),
        state=KES.calculator,
        getter=KES_getters.get_data_for_kes_calculator
    )


def input_window() -> Window:
    return Window(
        Format('{topic}'),
        TextInput(id='enter_data',
                  on_success=KES_selected.on_entered_parameter_value),
        SwitchTo(Const('<< назад'),
                 id='sw_to_in_menu',
                 state=KES.calculator),
        state=KES.parameter_value_input,
        getter=KES_getters.get_topic_for_input,
    )


def report_window() -> Window:
    return Window(
        Format('{result}'),
        # Const('результат в закрепленном сообщении'),
        SwitchTo(Const('<< изменить параметры'),
                 id='sw_to_input_menu',
                 state=KES.calculator),
        SwitchTo(Const('<< назад в меню функций'),
                 id='sw_to_func_menu',
                 state=KES.menu),
        Cancel(Const('задача решена!'),
               on_click=KES_selected.on_adieu),
        state=KES.report_menu,
        getter=KES_getters.get_report)

#
#def report_window() -> Window:
#    return Window(
#        Format('{result}'),
#        # Const('результат в закрепленном сообщении'),
#        SwitchTo(Const('<< изменить параметры'),
#                 id='sw_to_input_menu',
#                 state=PatientDataInput.patient_parameters_menu),
#        SwitchTo(Const('<< назад в меню функций'),
#                 id='sw_to_func_menu',
#                 state=PatientDataInput.func_menu,
#                 on_click=selected.on_send_report_msg),
#        SwitchTo(Const('задача решена!'),
#                 id='sw_to_finish_report',
#                 state=PatientDataInput.print_finish_session_report),
#        state=PatientDataInput.report_menu,
#        getter=getters.get_report)
#
#
#def finish_window():
#    return Window(
#        Format("{result}"),
#        Cancel(Const('до встречи!'),
#               on_click=selected.on_adieu),
#        state=PatientDataInput.print_finish_session_report,
#        getter=getters.get_report,
#    )


KES_dialog = Dialog(KES_menu_window(),
                    time_calculator_menu(),
                    input_window(),
                    report_window()
                    )
