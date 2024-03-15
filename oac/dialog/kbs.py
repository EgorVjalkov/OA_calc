import operator

from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Column, Row, Button, Back, Group, Checkbox
from aiogram_dialog.widgets.text import Const, Format


SCROLLING_HEIGHT = 1


def group_kb(on_click, group_id, select_id, select_items):
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


def group_kb_with_checkbox(on_click, variants, group_id):
    cb = checkboxes(variants, on_click)
    return Group(*cb,
                 id=group_id,
                 width=2)


def checkboxes(variants, on_click):
    checkboxes_list = []
    for text, id_ in variants:
        cb = Checkbox(
            Const(f'{text} [+]'),
            Const(f'{text}'),
            id=id_,
            on_click=on_click
        )
        checkboxes_list.append(cb)
    return checkboxes_list


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
