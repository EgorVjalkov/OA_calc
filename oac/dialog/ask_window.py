from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Start, Cancel, Back, SwitchTo
from aiogram_dialog.widgets.input.text import TextInput

from oac.dialog.states import FeedBack
from oac.dialog import kbs
from oac.dialog import selected
from oac.dialog import getters
from oac.dialog.variants_with_id import sma_confirm_text


def ask_window():
    return Window(
        Const('Задайте вопрос в свободной форме'),
        TextInput(id='ask',
                  on_success=selected.on_ask_a_question),
        Cancel(Const('<< назад')),
        state=FeedBack.ask_menu,
    )


feedback_dialog = Dialog(ask_window())
