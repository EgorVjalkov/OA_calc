from  prettytable import PrettyTable


def get_my_table_string(fields: list, rows: list, header: bool = True) -> str:
    my_table = PrettyTable(field_names=fields,
                           border=False,
                           align='l',
                           header=header,
                           )
    for r in rows:
        my_table.add_row(r)

    return my_table.get_string()
