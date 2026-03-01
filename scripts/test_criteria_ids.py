import asyncio
import logging
from unittest.mock import AsyncMock, MagicMock
from oac.dialogs.criteria_dialogs.getters import get_pathologies
from oac.dialogs.criteria_dialogs.handlers import on_pathology_selected
from oac.program_logic.criteria_service import criteria_service

logging.basicConfig(level=logging.INFO)

async def test_criteria_ids():
    # Test 1: get_pathologies returns short string IDs
    data = await get_pathologies()
    pathologies_list = data["pathologies"]
    
    # Assert we have items and they are tuples of (name, id)
    assert len(pathologies_list) > 0, "No pathologies loaded"
    
    for name, item_id in pathologies_list:
        # aiogram callbacks strict limit is 64 bytes. 
        # But here we used integer string IDs. Let's just check length.
        assert len(item_id.encode('utf-8')) < 64, f"ID {item_id} exceeds 64 bytes"
        assert item_id.isdigit(), f"ID {item_id} is not a digit string"
    
    print("✅ Test 1 Passed: All IDs are short digit strings (under 64 bytes)")

    # Test 2: on_pathology_selected properly sets the name
    # We will mock CallbackQuery, Select and DialogManager
    callback_mock = AsyncMock()
    widget_mock = MagicMock()
    dialog_manager_mock = AsyncMock()
    dialog_manager_mock.dialog_data = {}

    # Pick a random pathology from the list to test
    test_name, test_id = pathologies_list[0]
    
    await on_pathology_selected(callback_mock, widget_mock, dialog_manager_mock, test_id)
    
    assert dialog_manager_mock.dialog_data.get("selected_pathology_name") == test_name, \
        "Handler did not set the correct pathology name in dialog_data"
        
    print(f"✅ Test 2 Passed: Handler successfully mapped ID '{test_id}' to name '{test_name}'")

if __name__ == "__main__":
    asyncio.run(test_criteria_ids())
