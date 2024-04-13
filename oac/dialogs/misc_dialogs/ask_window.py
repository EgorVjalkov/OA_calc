from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.input.text import TextInput

from oac.dialogs.states import FeedBack
from oac.dialogs.misc_dialogs.ask_selected import on_click


def ask_window():
    return Window(
        Const('Задайте вопрос в свободной форме'),
        TextInput(id='ask',
                  on_success=on_click),
        Cancel(Const('<< назад')),
        state=FeedBack.ask_menu,
    )


feedback_dialog = Dialog(ask_window())
