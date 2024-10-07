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
    data = {'time_for_KES': kes.get_btns(), 'count_flag': False}
    if kes.all_params_filled:
        data['count_flag'] = True
    return data


async def get_topic_for_input(dialog_manager: DialogManager,
                              **middleware_date) -> Optional[dict]:
    kes = get_KES(dialog_manager)
    return {'topic': kes.current.topic}


async def get_report(dialog_manager: DialogManager,
                     **middleware_date) -> Optional[dict]:
    kes = get_KES(dialog_manager)
    return {'result': kes.get_answer()}

