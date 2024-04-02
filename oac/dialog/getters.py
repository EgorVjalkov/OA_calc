from typing import Optional

from aiogram_dialog import DialogManager
from aiogram.fsm.state import State

from oac.dialog.states import PatientDataInput
from oac.program_logic.function import PatientParameter, Function
from oac.program_logic.patient import Patient, ParametersForCurrentFunc
from oac.dialog.variants_with_id import get_dict_with_variants, variants
from oac.dialog.patientparameter import PatientParameter
from oac.dialog.selected import get_patient, set_patient


async def get_funcs(dialog_manager: DialogManager,
                    **middleware_data) -> dict:
    return get_dict_with_variants('funcs')


async def get_data_for_pat_params_menu(dialog_manager: DialogManager,
                                       **middleware_date) -> dict:
    patient = get_patient(dialog_manager)
    patient.set_current_params()
    return {'patient_parameters': patient.params.get_btns(), 'topic': patient.topic}


async def get_topic_for_input(dialog_manager: DialogManager,
                              **middleware_date) -> Optional[dict]:
    patient = get_patient(dialog_manager)
    return {'topic': patient.params.current.topic}


async def get_kb_for_select_parameter(dialog_manager: DialogManager,
                                      **middleware_data) -> dict:
    patient = get_patient(dialog_manager)
    return {'param_values': patient.params.current.get_btns(), 'topic': patient.params.current.topic}


async def get_report(dialog_manager: DialogManager,
                     **middleware_date) -> dict:
    ctx = dialog_manager.current_context()
    patient = get_patient(dialog_manager)

    match ctx.state, patient:
        case [State(state=PatientDataInput.print_report), p]:

            p.get_result()
            return {'result': patient.get_reports(last=True)}

        case [State(state=PatientDataInput.print_finish_session_report),
              Patient(is_results_empty=True)]:
            return {'result': 'Никаких задач, так никаких задач...'}

        case [State(state=PatientDataInput.print_finish_session_report),
              Patient(is_results_empty=False)]:
            return {'result': patient.get_reports()}

    return {'result': 'не сработало'}
