from typing import Iterable

import pandas as pd
from  prettytable import PrettyTable


#def get_my_table_string(rows: list, fields: Iterable = (), header: bool = True) -> str:
#    my_table = PrettyTable(field_names=fields,
#                           border=False,
#                           align='l',
#                           header=header,
#                           )
#    for r in rows:
#        my_table.add_row(r)
#
#    return my_table.get_string()

def get_my_table_string(rows: list, fields: Iterable = (), header: bool = True, divider: str = ' -> ') -> str:
    rows = [[str(i) for i in row] for row in rows]
    rows = [divider.join(i) for i in rows]
    if fields:
        divider2 = len(divider) * ' '
        rows.insert(0, divider2.join(fields))
    return '\n'.join(rows)

# def get_my_table_string(rows: list,
#                         fields: Iterable = (),
#                         divider: str = ' -> ',
#                         header: bool = False) -> str:
#     df = pd.DataFrame(rows)
#     print(df)
#     df = df.set_index(df.columns[0])
#     return str(df)






