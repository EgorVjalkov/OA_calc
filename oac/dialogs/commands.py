from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from aiogram_dialog import StartMode, DialogManager

from oac.dialogs.states import PatientDataInput, FeedBack
from oac.program_logic.patient import Patient

router = Router()


@router.message(Command('start'))
async def start_dialog(message: Message,
                       dialog_manager: DialogManager) -> None:
    await dialog_manager.start(PatientDataInput.func_menu,
                               data={'patient': Patient()},
                               mode=StartMode.RESET_STACK)


@router.message(Command('ask'))
async def ask(message: Message,
              dialog_manager: DialogManager) -> None:
    await dialog_manager.start(FeedBack.ask_menu)


@router.message(Command('theory'))
async def ask(message: Message,
              dialog_manager: DialogManager) -> None:
    await dialog_manager.start(FeedBack.ask_menu)
