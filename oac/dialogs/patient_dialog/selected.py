from typing import Optional

from aiogram import Bot
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select, Cancel, Button, SwitchTo
from aiogram_dialog.widgets.input.text import TextInput
from aiogram_dialog.api.exceptions import NoContextError
from fastnumbers import isreal, fast_real

from oac.My_token import TOKEN, ADMIN_ID
from oac.dialogs.states import PatientSession
from oac.dialogs.misc_dialogs.report_message import ReportMessage
from oac.program_logic.patient import Patient
from oac.program_logic.patientparameter import BaseParameter, LimitedParameter


def get_patient(dm: DialogManager) -> Optional[Patient]:
    try:
        ctx = dm.current_context()
        return ctx.start_data['patient']
    except NoContextError:
        return None



async def on_chosen_func(c: CallbackQuery,
                         w: Select,
                         dm: DialogManager,
                         item_id: str,
                         **kwargs) -> None: # рефактор
    if item_id != 'apacheII_count':
        patient: Patient = get_patient(dm)
        patient.func_id = item_id
        # set_patient(dm, patient)

        if item_id == 'sma_count':
            await dm.switch_to(state=PatientSession.sma_confirm)
        else:
            if patient.need_scrolling_params:
                await dm.switch_to(state=PatientSession.patient_parameters_menu_if_scrolling)
            else:
                await dm.switch_to(state=PatientSession.patient_parameters_menu)

    else:
        await dm.switch_to(state=PatientSession.apache_change)


async def on_chosen_apache_scale(c: CallbackQuery,
                                 w: Select,
                                 dm: DialogManager,
                                 item_id: str,
                                 **kwargs) -> None:

    patient: Patient = get_patient(dm)
    patient.func_id = item_id
    await dm.switch_to(state=PatientSession.patient_parameters_menu_if_scrolling)


async def on_chosen_patient_parameter(c: CallbackQuery,
                                      w: Select,
                                      dm: DialogManager,
                                      item_id: str,
                                      **kwargs) -> None:
    if 'count' in item_id:
        await dm.switch_to(state=PatientSession.report_menu)

    else:
        patient = get_patient(dm)
        patient.params.parameter_id = item_id
        if patient.params.current.fill_by_text_input == 'True':
            await dm.switch_to(state=PatientSession.value_textinput)
        else:
            await dm.switch_to(state=PatientSession.value_onclickinput)


async def on_entered_parameter_value(m: Message,
                                     w: TextInput,
                                     dm: DialogManager,
                                     input_data: str,
                                     **kwargs):

    # наверно можно упростить и дописать занчения
    value = input_data.replace(',', '.')

    if not isreal(value):
        return

    patient = get_patient(dm)
    value = fast_real(value)

    match patient.params.current:
        case LimitedParameter():
            if value in patient.params.current.limits:
                patient.params.current.value = value

        case BaseParameter():
            if value > 0:
                patient.params.current.value = value

    if patient.need_scrolling_params:
        await dm.switch_to(PatientSession.patient_parameters_menu_if_scrolling)
    else:
        await dm.switch_to(PatientSession.patient_parameters_menu)


async def on_back_to_params_menu(c: CallbackQuery,
                                 w: Button,
                                 dm: DialogManager,
                                 **kwargs):
    patient: Patient = get_patient(dm)
    if patient.need_scrolling_params:
        await dm.switch_to(PatientSession.patient_parameters_menu_if_scrolling)
    else:
        await dm.switch_to(PatientSession.patient_parameters_menu)


async def on_chosen_parameter_value(c: CallbackQuery,
                                    w: Select,
                                    dm: DialogManager,
                                    item_id: str,
                                    **kwargs):
    patient = get_patient(dm)
    patient.params.current.value = item_id
    if patient.need_scrolling_params:
        await dm.switch_to(PatientSession.patient_parameters_menu_if_scrolling)
    else:
        await dm.switch_to(PatientSession.patient_parameters_menu)


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

