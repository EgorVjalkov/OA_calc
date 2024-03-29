from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select, Cancel, Button
from aiogram_dialog.widgets.input.text import TextInput

from oac.dialog.states import PatientDataInput
from oac.program_logic.patient import Patient


def get_patient(dm: DialogManager) -> Patient:
    ctx = dm.current_context()
    return ctx.start_data['patient']


def set_patient(dm: DialogManager, patient: Patient) -> None:
    ctx = dm.current_context()
    ctx.start_data.update({'patient': patient})


async def on_chosen_func(c: CallbackQuery,
                         w: Select,
                         dm: DialogManager,
                         item_id: str,
                         **kwargs) -> None:
    patient: Patient = get_patient(dm)
    patient.func_id = item_id
    print(patient)
    if item_id == 'sma_count':
        await dm.switch_to(state=PatientDataInput.sma_confirm)
    else:
        await dm.switch_to(state=PatientDataInput.patient_parameters_menu)


async def on_chosen_patient_data(c: CallbackQuery,
                                 w: Select,
                                 dm: DialogManager,
                                 item_id: str,
                                 **kwargs) -> None:
    if 'count' in item_id:
        await dm.switch_to(state=PatientDataInput.print_report)

    else:
        patient = get_patient(dm)
        patient.params.parameter_id = item_id
        set_patient(dm, patient)

        if patient.params.current.fill_by_text_input:
            await dm.switch_to(state=PatientDataInput.parameter_value_input)
        else:
            await dm.switch_to(state=PatientDataInput.parameter_value_menu)


async def on_entered_parameter_value(m: Message,
                                     w: TextInput,
                                     dm: DialogManager,
                                     input_data: str,
                                     **kwargs):

    if not input_data.isdigit():
        await m.answer('Задайте число.')
        return

    patient = get_patient(dm)
    patient.params.current.value = int(input_data)
    print(patient.params.current.value, patient.params.current.button_text)
    print(patient.params.current)
    set_patient(dm, patient)
    await dm.switch_to(PatientDataInput.patient_parameters_menu)


async def on_chosen_parameter_value(m: CallbackQuery,
                                    w: Select,
                                    dm: DialogManager,
                                    item_id: str,
                                    **kwargs):
    ctx = dm.current_context()
    patient_data = ctx.dialog_data.get('patient_data')
    ctx.dialog_data.update({patient_data: item_id})
    await dm.switch_to(state=PatientDataInput.patient_parameters_menu)


async def on_adieu(c: CallbackQuery,
                   w: Cancel,
                   dm: DialogManager,
                   **kwargs):
    await dm.event.answer("До свидания!")
