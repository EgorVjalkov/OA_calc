from typing import Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

from oac.program_logic.parameters import ParametersForCurrentFunc
from oac.program_logic.patientparameter import DateTimeParameter
from oac.program_logic.my_table import get_my_table_string
from oac.dialogs.KES_dialog.KES_utils import MyTimeDelta, TimeInError, TimeOutError


@dataclass
class KesCalculator(ParametersForCurrentFunc):
    def __post_init__(self):
        super().__post_init__()
        self.set_current_params('kes_time_count')
        self.delta: Optional[timedelta] = None

    @staticmethod
    def convert(time_str: str) -> datetime:
        time = datetime.strptime(time_str, '%d.%m.%y %H:%M')
        return time

    @staticmethod
    def get_kes(hours) -> str:
        match hours:
            case h if h < 24:
                return '4310.10'
            case h if h < 72:
                return '4310.20'
        return '4310.30'

    def set_value(self, text_input: str):
        date_time = self.convert(text_input)
        match self.current.id, self.current_params:
            case 'time_out', {'time_in': t_in} if t_in.value:
                if date_time <= t_in.value_like_datetime:
                    raise TimeOutError(TimeOutError.message)

            case 'time_in', {'time_out': t_out} if t_out.value:
                if date_time >= t_out.value_like_datetime:
                    raise TimeInError(TimeInError.message)

        self.current.value = text_input
        self.current.value_like_datetime = date_time

    def get_answer(self):
        time_in: DateTimeParameter = self.current_params['time_in']
        time_out: DateTimeParameter = self.current_params['time_out']

        delta: timedelta = time_out.value_like_datetime - time_in.value_like_datetime
        delta_in_str = MyTimeDelta(delta)
        delta_in_str.normalize()

        hours = f'{delta_in_str.hours} ч.'
        minutes = f'{delta_in_str.minutes} мин.'
        in_unit = f'{hours} {minutes}'

        answer = [
            ['время поступления:', f'{time_in.value}'],
            ['время перевода:', f'{time_out.value}'],
            ['всего в отделении:', f'{in_unit}'],
            ['КЭС:', f'{self.get_kes(int(delta_in_str.hours))}']
        ]

        return get_my_table_string(answer, header=False)


