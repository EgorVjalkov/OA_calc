from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.input.text import TextInput

from oac.dialogs.states import FeedBack, Theory
from oac.dialogs.misc_dialogs import misc_selected
from oac.dialogs.misc_dialogs.misc_getters import get_theory


def ask_window():
    return Window(
        Const('Задайте вопрос в свободной форме'),
        TextInput(id='ask',
                  on_success=misc_selected.on_asking),
        Cancel(Const('не хочу'),
               on_click=misc_selected.on_del_window),
        state=FeedBack.ask_menu,
    )


feedback_dialog = Dialog(ask_window())


def theory_window() -> Window:
    return Window(
        Format('{theory}'),
        Cancel(Const('понятно')),
        state=Theory.theory,
        getter=get_theory
    )


theory_dialog = Dialog(theory_window())

