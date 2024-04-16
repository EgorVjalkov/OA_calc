from aiogram_dialog import DialogManager
from oac.dialogs.variants_with_id import func_theory
from oac.dialogs.selected import get_patient


async def get_theory(dialog_manager: DialogManager,
                     **middleware_data) -> dict:
    ctx = dialog_manager.current_context()
    func_id = ctx.start_data['func_id']
    print(func_id)
    return {'theory': func_theory[func_id]}


