from typing import Optional

from aiogram_dialog import DialogManager
from aiogram.fsm.state import State

from oac.dialogs.states import PatientSession
from oac.program_logic.patient import Patient
from oac.dialogs.variants_with_id import funcs, apaches
from oac.dialogs.patient_dialog.selected import get_patient


async def get_funcs(dialog_manager: DialogManager,
                    **middleware_data) -> dict:

    data = {'funcs': funcs}
    patient = get_patient(dialog_manager)
    patient.func_id = None
    if not patient.is_results_empty:
        data['finish'] = 'печать результатов'
    else:
        data['finish'] = 'спасибо, не надо'
    return data


async def get_apaches(dialog_manager: DialogManager,
                      **middleware_daa) -> dict:
    data = {'apaches': apaches}
    return data


async def get_data_for_params_menu(dialog_manager: DialogManager,
                                   **middleware_date) -> dict:
    patient = get_patient(dialog_manager)
    patient.set_current_params()
    data = {'patient_parameters': patient.params.get_btns(), 'topic': patient.topic, 'count_flag': False}
    if patient.params.all_params_filled:
        data['count_flag'] = True
    return data


async def get_topic_for_input(dialog_manager: DialogManager,
                              **middleware_date) -> Optional[dict]:
    patient = get_patient(dialog_manager)
    return {'topic': patient.params.current.topic}


async def get_data_for_onclickinput(dialog_manager: DialogManager,
                                    **middleware_data) -> dict:
    patient: Patient = get_patient(dialog_manager)
    print(patient.params.current.get_btns())
    return {'param_values': patient.params.current.get_btns(), 'topic': patient.params.current.topic}


async def get_report(dialog_manager: DialogManager,
                     **middleware_date) -> dict:
    ctx = dialog_manager.current_context()
    patient = get_patient(dialog_manager)
    data = {}

    match ctx.state, patient:
        case [State(state=PatientSession.report_menu), p]:
            p.change_func().get_result()
            # result = p.get_reports(last=True)
            # await dialog_manager.event.message.answer(result)
            data.update({'result': patient.get_reports(last=True)})

        case [State(state=PatientSession.print_finish_session_report),
              Patient(is_results_empty=True)]:
            data.update({'result': 'Обращайтесь!'})
            ctx.start_data.clear()

        case [State(state=PatientSession.print_finish_session_report),
              Patient(is_results_empty=False)]:
            data.update({'result': patient.get_reports()})
            ctx.start_data.clear()

    return data
