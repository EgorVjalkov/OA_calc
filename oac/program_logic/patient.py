import pandas as pd
from oac.program_logic.function import Function
from typing import Optional


class Patient:
    def __init__(self):
        self.parameters = {}
        self.functions = {}
        self.reports = {}
        self.function_id: Optional[str] = None

    @property
    def func_id(self):
        return self.function_id

    @func_id.setter
    def func_id(self, id):
        self.function_id = id
