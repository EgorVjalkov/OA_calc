from typing import Iterable
from  prettytable import PrettyTable


def get_my_table_string(rows: list, fields: Iterable = (), header: bool = True) -> str:
    my_table = PrettyTable(field_names=fields,
                           border=False,
                           align='l',
                           header=header,
                           )
    for r in rows:
        my_table.add_row(r)

    return my_table.get_string()
