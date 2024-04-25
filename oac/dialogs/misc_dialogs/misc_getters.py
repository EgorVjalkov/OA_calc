from aiogram.fsm.state import State
from aiogram_dialog import DialogManager

from oac.dialogs.variants_with_id import func_theory
from oac.dialogs.states import PatientDataInput
from oac.dialogs.misc_dialogs.report_message import ReportMessage
from oac.program_logic.patient import Patient


async def get_theory(dialog_manager: DialogManager,
                     **middleware_data) -> dict:
    ctx = dialog_manager.current_context()
    func_id = ctx.start_data['func_id']
    print(func_id)
    return {'theory': func_theory[func_id]}


async def update_report_message(dialog_manager: DialogManager,
                                **middleware_date) -> None:
    ctx = dialog_manager.current_context()
    patient: Patient = ctx.start_data.get('patient')
    rep_msg: ReportMessage = ctx.start_data.get('rep_msg')
    print(rep_msg)
    print(patient)
    print(ctx.state)

    match ctx.state, patient:
        case [State(state=PatientDataInput.report_menu), p]:
            p.change_func().get_result()
            await rep_msg.send_n_pin(patient.get_reports())

        case [State(state=PatientDataInput.print_finish_session_report),
              Patient(is_results_empty=True)]:
            await rep_msg.send_n_pin(patient.get_reports())

        case [State(state=PatientDataInput.print_finish_session_report),
              Patient(is_results_empty=True)]:
            pass
            # await rep_msg.del_rep_msg()
