from aiogram.fsm.state import State
from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import SwitchTo, Group, ScrollingGroup
from aiogram_dialog.widgets.input import TextInput

from oac.dialogs.states import PatientDataInput
from oac.dialogs.patient_dialog import getters
from oac.dialogs.patient_dialog import kbs, selected


class ParamsWindow(Window):
    def __init__(self,
                 keyboard: Group | ScrollingGroup,
                 state: State):
        super().__init__(
            Format('{topic}'),
            keyboard,
            SwitchTo(Const('<< назад'),
                     id='sw_back',
                     state=PatientDataInput.func_menu),
            state=state,
            getter=getters.get_data_for_params_menu,
        )


class ParamKbInputWindow(Window):
    def __init__(self,
                 state: State,
                 state_for_change_params: State):
        super().__init__(
            Format('{topic}'),
            TextInput(id='enter_data',
                      on_success=selected.on_entered_parameter_value),
            SwitchTo(Const('<< назад'),
                     id='sw_to_in_menu',
                     state=state_for_change_params),
            state=state,
            getter=getters.get_topic_for_input,
        )


class ParamOnClickInputWindow(Window):
    def __init__(self,
                 state: State,
                 state_for_change_params: State):
        super().__init__(
            Format('{topic}'),
            kbs.Keyboard('simple_by_attr', 'value', 'param_values'
                         ).get_kb(selected.on_chosen_parameter_value),
            SwitchTo(Const('<< назад'),
                     id='sw_to_in_menu',
                     state=state_for_change_params),
            state=state,
            getter=getters.get_kb_for_select_parameter,
        )


class ReportWindow(Window):
    def __init__(self,
                 state,
                 state_for_change_params):
        super().__init__(
            Format('{result}'),
            # Const('результат в закрепленном сообщении'),
            SwitchTo(Const('<< изменить параметры'),
                     id='sw_to_input_menu',
                     state=state_for_change_params),
            SwitchTo(Const('<< назад в меню функций'),
                     id='sw_to_func_menu',
                     state=PatientDataInput.func_menu),
            # on_click=selected.on_send_report_msg), # закреп себя не оправдал. быть может нужно через другого бота...
            SwitchTo(Const('задача решена!'),
                     id='sw_to_finish_report',
                     state=PatientDataInput.print_finish_session_report),
            state=state,
            getter=getters.get_report
        )
