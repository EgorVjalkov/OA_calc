from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Select

from oac.dialogs.states import CriteriaSG
from oac.program_logic.criteria_service import criteria_service

async def on_mode_selected(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Обработчик выбора режима (Критерии или Рекомендации)."""
    mode = button.widget_id  # 'btn_criteria' or 'btn_recommendations'
    dialog_manager.dialog_data["mode"] = "criteria" if mode == "btn_criteria" else "recommendations"
    await dialog_manager.switch_to(CriteriaSG.select_pathology)

async def on_pathology_selected(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    """Обработчик выбора патологии из списка."""
    mode = dialog_manager.dialog_data.get("mode", "criteria")
    
    if mode == "criteria":
        pathologies = criteria_service.get_all_criteria_pathologies()
    else:
        pathologies = criteria_service.get_all_recommendation_pathologies()
        
    try:
        idx = int(item_id)
        if 0 <= idx < len(pathologies):
            dialog_manager.dialog_data["selected_pathology_name"] = pathologies[idx]
            dialog_manager.dialog_data["recs_page"] = 0
            await dialog_manager.switch_to(CriteriaSG.view_criteria)
        else:
            await callback.answer("Ошибка: патология не найдена", show_alert=True)
    except ValueError:
        await callback.answer("Ошибка: неверный ID", show_alert=True)

async def on_back_clicked(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Обработчик кнопки Назад: возвращает к списку."""
    await dialog_manager.switch_to(CriteriaSG.select_pathology)

async def on_back_to_menu_clicked(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Обработчик кнопки Назад в меню выбора режима."""
    await dialog_manager.switch_to(CriteriaSG.mode_selection)

async def on_done_clicked(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Обработчик кнопки Готово: закрывает диалог."""
    await dialog_manager.done()

async def on_prev_page(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Листаем страницу рекомендаций назад."""
    page = dialog_manager.dialog_data.get("recs_page", 0)
    dialog_manager.dialog_data["recs_page"] = max(0, page - 1)

async def on_next_page(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Листаем страницу рекомендаций вперед."""
    page = dialog_manager.dialog_data.get("recs_page", 0)
    dialog_manager.dialog_data["recs_page"] = page + 1
