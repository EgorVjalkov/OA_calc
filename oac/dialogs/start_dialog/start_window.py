from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Start, Cancel, Back, SwitchTo
from aiogram_dialog.widgets.input.text import TextInput

from oac.dialogs.states import MainMenu
from oac.dialogs import kbs
from oac.dialogs import selected
from oac.dialogs import getters
from oac.dialogs.variants_with_id import sma_confirm_text


def greet_window() -> Window:
    return Window(
        Const('Привет, я - бот для расчетов в акушерской анестезиологии. '
              'Выберите функцию.'),
        kbs.group_kb_by_item(selected.on_chosen_func,
                             'func', 'funcs'),
        SwitchTo(Format('{finish}'),
                 id='sw_finish',
                 state=),
        state=MainMenu.func_menu,
        getter=getters.get_funcs,
    )

