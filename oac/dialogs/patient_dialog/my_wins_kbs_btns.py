import operator
from dataclasses import dataclass

from aiogram.fsm.state import State
from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import SwitchTo, Group, ScrollingGroup, Button, Select

from oac.dialogs.states import PatientSession
from oac.dialogs.patient_dialog import getters


SCROLLING_HEIGHT = 5


class ParamsWindow(Window):
    def __init__(self,
                 keyboard: Group | ScrollingGroup,
                 state: State):
        super().__init__(
            Format('{topic}'),
            keyboard,
            SwitchTo(Const('рассчитать'),
                     id='count',
                     state=PatientSession.report_menu,
                     when='count_flag'),
            SwitchTo(Const('<< назад'),
                     id='sw_back',
                     state=PatientSession.func_menu),
            state=state,
            getter=getters.get_data_for_params_menu,
        )


class MyBackButton(Button):
    def __init__(self, on_click, text: str = '<< назад'):
        super().__init__(
            Const(text),
            id='back',
            on_click=on_click
        )


class MySelectByItem(Select):
    def __init__(self, on_click, select_id: str, select_items: str):
        super().__init__(
            Format('{item[0]}'),
            id=select_id,
            item_id_getter=operator.itemgetter(1),
            items=select_items,
            on_click=on_click
        )


class MySelectByAttr(Select):
    def __init__(self, on_click, select_id: str, select_items: str):
        super().__init__(
            Format('{item.text}'),  #
            id=select_id,
            item_id_getter=operator.attrgetter('id'),
            items=select_items,
            on_click=on_click
        ),


@dataclass
class Keyboard:
    mode: str
    id_postfix: str
    select_items: str

    def get_kb(self, on_click) -> Group | ScrollingGroup:
        group_id = f'g_{self.id_postfix}'
        select_id = f's_{self.id_postfix}'
        match self.mode:
            case 'scroll_by_attr':
                return ScrollingGroup(
                    MySelectByAttr(on_click, select_id, self.select_items),
                    id=group_id,
                    width=1,
                    height=SCROLLING_HEIGHT
                )
            case 'simple_by_attr':
                return Group(
                    MySelectByAttr(on_click, select_id, self.select_items),
                    id=group_id,
                    width=1
                )
            case 'simple_by_item':
                return Group(
                    MySelectByItem(on_click, select_id, self.select_items),
                    id=group_id,
                    width=1
                )

