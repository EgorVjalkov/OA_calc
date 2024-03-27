from collections import namedtuple
from typing import Dict, Any

import pandas as pd


def load_parameters(func_id) -> dict:
    params_dict = {}
    path = 'parameters.xlsx'
    # path = 'dialog/parameters.xlsx'
    param_df = pd.read_excel(path, sheet_name='parameters', dtype=object)
    filtered = param_df.func_id.map(lambda i: func_id in i)
    param_df = param_df[filtered == True]
    del param_df['func_id']

    PatientParameter = namedtuple('PatientParameter',
                                  field_names=param_df.columns.to_list())

    for param_row in param_df.index:
        row = param_df.loc[param_row]
        parameter = PatientParameter(**row.to_dict())
        params_dict[parameter.id] = parameter
    return params_dict


df = load_parameters('sma_count')
print(df)
