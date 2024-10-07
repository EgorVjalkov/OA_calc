from typing import Optional

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select, Button
from aiogram_dialog.widgets.input.text import TextInput
from aiogram_dialog.api.exceptions import NoContextError

from oac.dialogs.states import KES
from oac.dialogs.KES_dialog.KES_calculator import KesCalculator, TimeInError, TimeOutError


def get_KES(dm: DialogManager) -> Optional[KesCalculator]:
    try:
        ctx = dm.current_context()
        return ctx.start_data['kes']
    except NoContextError:
        return None


def set_KES(dm: DialogManager, kes: KesCalculator) -> None:
    ctx = dm.current_context()
    ctx.start_data.update({'kes': kes})


async def on_chosen_kes_parameter(c: CallbackQuery,
                                  w: Select,
                                  dm: DialogManager,
                                  item_id: str,
                                  **kwargs) -> None:
    if 'count' in item_id:
        await dm.switch_to(state=KES.report_menu)

    else:
        kes = get_KES(dm)
        kes.parameter_id = item_id
        set_KES(dm, kes)
        await dm.switch_to(state=KES.parameter_value_input)


async def on_entered_parameter_value(m: Message,
                                     w: TextInput,
                                     dm: DialogManager,
                                     input_data: str,
                                     **kwargs):
    kes: KesCalculator = get_KES(dm)
    try:
        kes.set_value(input_data)

    except ValueError:
        await m.answer('Недопустимое значение')
        return

    except TimeInError:
        await m.answer(TimeInError.message)
        return

    except TimeOutError:
        await m.answer(TimeOutError.message)
        return

    set_KES(dm, kes)
    await dm.switch_to(KES.calculator)


async def on_adieu(c: CallbackQuery,
                   w: Button,
                   dm: DialogManager,
                   **kwargs):
    await dm.event.answer("До свидания!")

