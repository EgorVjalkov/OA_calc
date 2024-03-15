from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command

from aiogram_dialog import StartMode, DialogManager
from aiogram_dialog.widgets.text import Format

from oac.dialog.states import PatientDataInput
from oac.dialog.drag import get_drag_list_answer


router = Router()


@router.message(Command('start'))
async def start_dialog(message: Message,
                       dialog_manager: DialogManager) -> None:
    # rep = get_drag_list_answer('dialog/drag_dosage.xlsx', 86)
    # await message.answer(rep)
    await dialog_manager.start(PatientDataInput.func_menu,
                               mode=StartMode.RESET_STACK)
