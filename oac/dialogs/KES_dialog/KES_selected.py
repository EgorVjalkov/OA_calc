from typing import Optional

from aiogram import Bot
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select, Cancel, Button, SwitchTo
from aiogram_dialog.widgets.input.text import TextInput
from aiogram_dialog.api.exceptions import NoContextError

from oac.My_token import TOKEN, ADMIN_ID
from oac.dialogs.states import KES
from oac.dialogs.misc_dialogs.report_message import ReportMessage
from oac.program_logic.patientparameter import BaseParameter, LimitedParameter
from oac.dialogs.KES_dialog.KES_calculator import KesCalculator


def get_KES(dm: DialogManager) -> Optional[KesCalculator]:
    try:
        ctx = dm.current_context()
        return ctx.start_data['kes']
    except NoContextError:
        return None


def set_KES(dm: DialogManager, kes: KesCalculator) -> None:
    ctx = dm.current_context()
    ctx.start_data.update({'kes': kes})


async def on_chosen_patient_parameter(c: CallbackQuery,
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
    if not kes.is_usable_format(input_data):
        await m.answer("Недопустимое значение")
        return

    kes.current.value = input_data
    set_KES(dm, kes)
    await dm.switch_to(KES.calculator)


async def on_chosen_parameter_value(m: CallbackQuery,
                                    w: Select,
                                    dm: DialogManager,
                                    item_id: str,
                                    **kwargs):
    patient = get_patient(dm)
    patient.params.current.value = item_id
    print(patient.params.current.value, patient.params.current.button_text)
    print(patient.params.current)
    set_patient(dm, patient)
    await dm.switch_to(state=PatientDataInput.patient_parameters_menu)


async def on_send_report_msg(c: CallbackQuery,
                             w: SwitchTo,
                             dm: DialogManager,
                             **kwargs):
    patient = get_patient(dm)
    report = patient.get_reports()
    rep_msg: ReportMessage = dm.dialog_data.get('rep_msg')
    if rep_msg:
        await rep_msg.edit(report)
    else:
        bot = Bot(TOKEN)
        user_id = c.from_user.id
        msg: Message = await dm.event.message.answer(report)
        await bot.pin_chat_message(c.from_user.id, msg.message_id)
        dm.dialog_data.update({'rep_msg': ReportMessage(user_id, msg.message_id, bot)})


async def on_adieu(c: CallbackQuery,
                   w: Button,
                   dm: DialogManager,
                   **kwargs):
    await dm.event.answer("До свидания!")

