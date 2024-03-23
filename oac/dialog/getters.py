from aiogram_dialog import DialogManager
from typing import Optional


from oac.dialog.states import PatientDataInput
from oac.program_logic.function import PatientParameter, Function
from oac.program_logic.patient import Patient
from oac.dialog.variants_with_id import get_dict_with_variants


async def get_funcs(dialog_manager: DialogManager,
                    **middleware_data) -> dict:
    return get_dict_with_variants('funcs')


async def get_variants(dialog_manager: DialogManager,
                       **middleware_date) -> dict:
    ctx = dialog_manager.current_context()
    patient = ctx.start_data['patient']
    patient.match_ctx_data(ctx.dialog_data)
    return {'patient_parameters': patient.variants_for_tg, 'topic': patient.topic}


async def get_topics_for_input(dialog_manager: DialogManager,
                               **middleware_date) -> Optional[dict]:
    ctx = dialog_manager.current_context()
    patient_data = ctx.dialog_data.get('patient_data')
    if not patient_data:
        await dialog_manager.event.answer('Выберите показатель для заполнения')
        await dialog_manager.switch_to(PatientDataInput.input_patient_data_menu)
        return
    else:
        category = PatientParameter(patient_data)
        data = {'category': category}
        return data


async def get_report(dialog_manager: DialogManager,
                     **middleware_date) -> dict:
    ctx = dialog_manager.current_context()
    patient: Patient = ctx.start_data['patient']

    match patient:
        case Patient(func_is_ready=False, results={}:
            return {'result': result}

        case [Patient(func_is_ready=True), _]:
            func_result = patient.func()
            result_data = {'result': '\n'.join(func_result)}
            ctx.dialog_data.update(result_data)
            return result_data

        case[Patient(func_is_ready=False), d] if 'func_result' not in d:
            return {'result': 'Никаких задач, так никаних задач...'}

    return {'result': 'не сработало'}
