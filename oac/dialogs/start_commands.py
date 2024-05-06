from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from aiogram_dialog import StartMode, DialogManager

from oac.dialogs.states import PatientDataInput, FeedBack, Theory, KES
from oac.program_logic.patient import Patient
from oac.dialogs.patient_dialog.selected import get_patient
from oac.dialogs.KES_dialog.KES_calculator import KesCalculator

router = Router()


@router.message(Command('new patient'))
async def start_dialog(message: Message,
                       dialog_manager: DialogManager) -> None:
    await dialog_manager.start(PatientDataInput.func_menu,
                               data={'patient': Patient()},
                               mode=StartMode.RESET_STACK)


@router.message(Command('kes'))
async def kes(message: Message,
              dialog_manager: DialogManager) -> None:
    await dialog_manager.start(KES.menu,
                               data={'kes': KesCalculator()})


@router.message(Command('ask'))
async def ask(message: Message,
              dialog_manager: DialogManager) -> None:
    await dialog_manager.start(FeedBack.ask_menu)


@router.message(Command('theory'))
async def ask(message: Message,
              dialog_manager: DialogManager) -> None:
    patient = get_patient(dialog_manager)
    match patient:
        case None:
            await message.answer('Сначала выберите функцию')
            await start_dialog(message, dialog_manager)
        case Patient(func_id=None):
            await message.answer('Сначала выберите функцию')
        case Patient(func_id=f_id):
            await dialog_manager.start(Theory.theory,
                                       data={'func_id': f_id})

