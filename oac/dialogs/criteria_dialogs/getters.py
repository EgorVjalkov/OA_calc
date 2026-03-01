from oac.program_logic.criteria_service import criteria_service

async def get_pathologies(dialog_manager, **kwargs):
    """Возвращает список патологий для окна выбора в зависимости от выбранного режима."""
    mode = dialog_manager.dialog_data.get("mode", "criteria")
    
    if mode == "criteria":
        pathologies = criteria_service.get_all_criteria_pathologies()
    else:
        pathologies = criteria_service.get_all_recommendation_pathologies()
        
    # aiogram-dialog Select expects a list of items. We pass (name, stringified index)
    # to avoid BUTTON_DATA_INVALID error in Telegram (max 64 bytes for callback data).
    return {
        "pathologies": [(p, str(i)) for i, p in enumerate(pathologies)],
        "mode_title": "Критерии качества" if mode == "criteria" else "Клинические рекомендации"
    }

async def get_criteria_text(dialog_manager, **kwargs):
    """Возвращает текст для выбранной патологии (критерии или рекомендации)."""
    mode = dialog_manager.dialog_data.get("mode", "criteria")
    pathology = dialog_manager.dialog_data.get("selected_pathology_name", "Не выбрано")
    
    is_criteria = (mode == "criteria")
    criteria_text = ""
    recs_list = []
    
    if is_criteria:
        criteria_text = criteria_service.get_criteria(pathology)
        if not criteria_text:
            criteria_text = "Критерии для данной патологии не найдены."
    else:
        recs = criteria_service.get_recommendations(pathology)
        if not recs:
            criteria_text = "Рекомендации для данной патологии не найдены."
        else:
            page = dialog_manager.dialog_data.get("recs_page", 0)
            page_size = 3
            
            for r in recs:
                item_text = f"<b>{r['short_level']}:</b> {r['text']} (стр. {r['page']})"
                recs_list.append(item_text)
                
            total_pages = (len(recs_list) + page_size - 1) // page_size
            # Ensure page is within bounds
            if page >= total_pages:
                page = max(0, total_pages - 1)
                dialog_manager.dialog_data["recs_page"] = page
                
            has_next = page < total_pages - 1
            has_prev = page > 0
            
            current_page_recs = recs_list[page*page_size : (page+1)*page_size]
            recs_text_str = "\n\n".join(current_page_recs)
            
            if total_pages > 1:
                recs_text_str += f"\n\n<i>Страница {page+1} из {total_pages}</i>"

    return {
        "is_criteria": is_criteria,
        "is_recs": not is_criteria,
        "pathology": pathology,
        "criteria_text": criteria_text,
        "recs_text": recs_text_str if not is_criteria else "",
        "has_prev": has_prev if not is_criteria else False,
        "has_next": has_next if not is_criteria else False,
    }
