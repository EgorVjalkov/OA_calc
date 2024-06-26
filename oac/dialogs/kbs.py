import operator

from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Group
from aiogram_dialog.widgets.text import Format

SCROLLING_HEIGHT = 1


def group_kb_by_attr(on_click, id_: str, select_items: str, ):
    group_id = f'g_{id_}'
    select_id = f's_{id_}'
    return Group(
        Select(
            Format('{item.text}'), #
            id=select_id,
            item_id_getter=operator.attrgetter('id'),
            items=select_items,
            on_click=on_click
        ),
        id=group_id,
        width=1
    )


def group_kb_by_item(on_click, id_: str, select_items: str):
    group_id = f'g_{id_}'
    select_id = f's_{id_}'
    return Group(
        Select(
            Format('{item[0]}'),
            id=select_id,
            item_id_getter=operator.itemgetter(1),
            items=select_items,
            on_click=on_click
        ),
        id=group_id,
        width=1
    )


def paginated_kb(on_click):
    return ScrollingGroup(
        Select(
            Format('{item[0]}'),
            id='s_scroll_funcs',
            item_id_getter=operator.itemgetter(1),
            items='funcs',
            on_click=on_click
        ),
        id='func_ids',
        width=1, height=SCROLLING_HEIGHT,
    )
