from typing import Optional

from aiogram_dialog import DialogManager
from aiogram.fsm.state import State

from oac.dialogs.states import PatientDataInput
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
        data['finish'] = 'никаких задач'
    return data


async def get_apaches(dialog_manager: DialogManager,
                      **middleware_daa) -> dict:
    data = {'apaches': apaches}
    return data


async def get_data_for_params_menu(dialog_manager: DialogManager,
                                   **middleware_date) -> dict:
    patient = get_patient(dialog_manager)
    state = dialog_manager.current_context().state
    print(state)
    patient.set_current_params()
    return {'patient_parameters': patient.params.get_btns(), 'topic': patient.topic}


async def get_topic_for_input(dialog_manager: DialogManager,
                              **middleware_date) -> Optional[dict]:
    patient = get_patient(dialog_manager)
    state = dialog_manager.current_context().state
    print(state)
    return {'topic': patient.params.current.topic}


async def get_kb_for_select_parameter(dialog_manager: DialogManager,
                                      **middleware_data) -> dict:
    patient = get_patient(dialog_manager)
    state = dialog_manager.current_context().state
    print(state)
    return {'param_values': patient.params.current.get_btns(), 'topic': patient.params.current.topic}


async def get_report(dialog_manager: DialogManager,
                     **middleware_date) -> dict:
    ctx = dialog_manager.current_context()
    patient = get_patient(dialog_manager)
    print(ctx.state)

    match ctx.state, patient:
        case [State(state=PatientDataInput.report_menu), p]:
            p.change_func().get_result()
            # result = p.get_reports(last=True)
            # await dialog_manager.event.message.answer(result)
            return {'result': patient.get_reports(last=True)}

        case [State(state=PatientDataInput.print_finish_session_report),
              Patient(is_results_empty=True)]:
            return {'result': 'Никаких задач, так никаких задач...'}

        case [State(state=PatientDataInput.print_finish_session_report),
              Patient(is_results_empty=False)]:
            return {'result': patient.get_reports()}

    return {'result': 'не сработало'}
