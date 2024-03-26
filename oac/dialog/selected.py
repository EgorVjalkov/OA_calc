from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select, Cancel, Button
from aiogram_dialog.widgets.input.text import TextInput

from oac.dialog.states import PatientDataInput
from oac.program_logic.spinal_dosage import Patient
from oac.dialog.getters import get_report


async def on_choosen_func(c: CallbackQuery,
                          w: Select,
                          dm: DialogManager,
                          item_id: str,
                          **kwargs) -> None:
    ctx = dm.current_context()
    ctx.dialog_data.update(func_id=item_id)
    if item_id == 'sma_count':
        await dm.switch_to(state=PatientDataInput.sma_confirm)
    else:
        await dm.switch_to(state=PatientDataInput.input_patient_data_menu)


async def bye(c: CallbackQuery,
              w: Cancel,
              dm: DialogManager,
              **kwargs):
    await dm.event.answer("До свидания!")


async def on_chosen_patient_data(c: CallbackQuery,
                                 w: Select,
                                 dm: DialogManager,
                                 item_id: str,
                                 **kwargs) -> None:
    if 'count' in item_id:
        await dm.switch_to(state=PatientDataInput.report)

    else:
        ctx = dm.current_context()
        ctx.dialog_data.update(patient_data=item_id)
        print(ctx.dialog_data)

        if item_id in ['fetus', 'bladder', 'discomfort']:
            await dm.switch_to(state=PatientDataInput.select_parameter)

        else:
            await dm.switch_to(state=PatientDataInput.input_parameter)


async def on_entered_data(m: Message,
                          w: TextInput,
                          dm: DialogManager,
                          input_data: str,
                          **kwargs):

    if not input_data.isdigit():
        await m.answer('Задайте число.')
        return

    input_data = int(input_data)
    ctx = dm.current_context()
    patient_data = ctx.dialog_data.get('patient_data') # <- здесь еще нужны лимиты типа женщина не может весить 20 кг и т.д
    ctx.dialog_data.update({patient_data: input_data})
    await dm.switch_to(PatientDataInput.input_patient_data_menu)


async def on_choosen_parameter(m: CallbackQuery,
                               w: Select,
                               dm: DialogManager,
                               item_id: str,
                               **kwargs):
    ctx = dm.current_context()
    patient_data = ctx.dialog_data.get('patient_data')
    ctx.dialog_data.update({patient_data: item_id})
    await dm.switch_to(state=PatientDataInput.input_patient_data_menu)


