from aiogram import Router
from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Select, ScrollingGroup, Button, Cancel, ListGroup, Row
from aiogram_dialog.widgets.text import Const, Format, List
import operator
import operator

from oac.dialogs.states import CriteriaSG
from oac.dialogs.criteria_dialogs.getters import get_pathologies, get_criteria_text
from oac.dialogs.criteria_dialogs.handlers import (
    on_mode_selected, 
    on_pathology_selected, 
    on_back_clicked, 
    on_done_clicked,
    on_back_to_menu_clicked,
    on_prev_page,
    on_next_page
)

router = Router()

mode_selection_window = Window(
    Const("<b>База медицинских знаний</b>\n\nВыберите раздел для просмотра:\n"
          "🔹 <b>Критерии качества</b> - табличные выжимки критериев оценки.\n"
          "🔹 <b>Сильные рекомендации</b> - тезисы (УУР А и В) из текста рекомендаций."),
    Button(
        Const("Критерии качества"),
        id="btn_criteria",
        on_click=on_mode_selected
    ),
    Button(
        Const("Сильные рекомендации (А/В)"),
        id="btn_recommendations",
        on_click=on_mode_selected
    ),
    Cancel(Const("❌ Закрыть")),
    state=CriteriaSG.mode_selection,
    parse_mode="HTML"
)

select_window = Window(
    Format("<b>{mode_title}: Выберите патологию</b>\n"),
    ScrollingGroup(
        Select(
            Format("{item[0]}"),
            id="pathology_select",
            item_id_getter=operator.itemgetter(1),
            items="pathologies",
            on_click=on_pathology_selected,
        ),
        id="pathology_scroll",
        width=1,
        height=8,
    ),
    Button(
        Const("<< в главное меню"),
        id="btn_back_menu",
        on_click=on_back_to_menu_clicked
    ),
    Cancel(Const("❌ Закрыть")),
    state=CriteriaSG.select_pathology,
    getter=get_pathologies,
    parse_mode="HTML"
)

view_window = Window(
    Format("<b>{pathology}</b>\n"),
    
    # Text for Criteria Mode (or if Recs mode has an error/empty state)
    Format("{criteria_text}", when="criteria_text"),
    
    # Paginated List of Recommendations for Recs Mode (rendered as text)
    Format("{recs_text}", when="is_recs"),
    
    Row(
        Button(
            Const("⬅️ Назад"),
            id="btn_recs_prev",
            on_click=on_prev_page,
            when="has_prev"
        ),
        Button(
            Const("Вперед ➡️"),
            id="btn_recs_next",
            on_click=on_next_page,
            when="has_next"
        )
    ),
    
    Button(
        Const("<< назад к списку"),
        id="btn_back",
        on_click=on_back_clicked,
    ),
    Button(
        Const("готово"),
        id="btn_done",
        on_click=on_done_clicked,
    ),
    state=CriteriaSG.view_criteria,
    getter=get_criteria_text,
    parse_mode="HTML"
)

criteria_dialog = Dialog(mode_selection_window, select_window, view_window)
router.include_router(criteria_dialog)
