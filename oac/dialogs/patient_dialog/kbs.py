import operator
from dataclasses import dataclass

from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Group
from aiogram_dialog.widgets.text import Format

SCROLLING_HEIGHT = 5


class MySelectByItem(Select):
    def __init__(self, on_click, select_id: str, select_items: str):
        super().__init__(
            Format('{item[0]}'),
            id=select_id,
            item_id_getter=operator.itemgetter(1),
            items=select_items,
            on_click=on_click
        )


class MySelectByAttr(Select):
    def __init__(self, on_click, select_id: str, select_items: str):
        super().__init__(
            Format('{item.text}'),  #
            id=select_id,
            item_id_getter=operator.attrgetter('id'),
            items=select_items,
            on_click=on_click
        ),


@dataclass
class Keyboard:
    mode: str
    id_postfix: str
    select_items: str

    def get_kb(self, on_click) -> Group | ScrollingGroup:
        group_id = f'g_{self.id_postfix}'
        select_id = f's_{self.id_postfix}'
        match self.mode:
            case 'scroll_by_attr':
                return ScrollingGroup(
                    MySelectByAttr(on_click, select_id, self.select_items),
                    id=group_id,
                    width=1,
                    height=SCROLLING_HEIGHT
                )
            case 'simple_by_attr':
                return Group(
                    MySelectByAttr(on_click, select_id, self.select_items),
                    id=group_id,
                    width=1
                )
            case 'simple_by_item':
                return Group(
                    MySelectByItem(on_click, select_id, self.select_items),
                    id=group_id,
                    width=1
                )


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
        width=1,
    )


def scroll_group_kb_by_attr(on_click, id_: str, select_items: str, ):
    group_id = f'g_{id_}'
    select_id = f's_{id_}'
    return ScrollingGroup(
        Select(
            Format('{item.text}'), #
            id=select_id,
            item_id_getter=operator.attrgetter('id'),
            items=select_items,
            on_click=on_click
        ),
        id=group_id,
        width=1,
        height=SCROLLING_HEIGHT
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
