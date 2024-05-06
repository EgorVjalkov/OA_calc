from typing import Optional

from aiogram_dialog import DialogManager
from aiogram.fsm.state import State

from oac.dialogs.states import KES
from oac.program_logic.patientparameter import Btn
from oac.dialogs.variants_with_id import KES_btns
from oac.dialogs.KES_dialog.KES_selected import get_KES


async def get_data_for_kes_calculator(dialog_manager: DialogManager,
                           **middleware_date) -> dict:
    kes = get_KES(dialog_manager)
    return {'patient_parameters': kes.get_btns()}


async def get_topic_for_input(dialog_manager: DialogManager,
                              **middleware_date) -> Optional[dict]:
    patient = get_patient(dialog_manager)
    return {'topic': patient.params.current.topic}
