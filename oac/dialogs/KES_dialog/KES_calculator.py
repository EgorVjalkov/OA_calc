from typing import Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from collections import namedtuple

from oac.program_logic.parameters import ParametersForCurrentFunc
from oac.program_logic.my_table import get_my_table_string


MyTimeDelta = namedtuple('MyTimeDelta', 'hours minutes')


class TimeError(Exception):
    message = ''


class TimeOutError(TimeError):
    message = 'время выбытия должно быть больше, чем время приема'


class TimeInError(Exception):
    message = 'время приема должно быть меньше, чем время приема'


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
            case h if h < 25:
                return 'нК4310.10'
            case h if h < 72:
                return 'нК4310.20'
        return 'нК4310.30'

    def set_value(self, text_input: str):
        date_time = self.convert(text_input)
        # не перезаписывает. а такеж проблемка с конверсией при выводе ответа
        match self.current, self.get_values():
            case {'time_in': 0, 'time_out': 0}:
                self.current.value = date_time

            case {'time_in': t_in, 'time_out': 0} if isinstance(t_in, datetime):
                if date_time > t_in:
                    self.current.value = date_time
                else:
                    raise TimeOutError(TimeOutError.message)

            case {'time_in': 0, 'time_out': t_out} if isinstance(t_out, datetime):
                if date_time < t_out:
                    self.current.value = date_time
                else:
                    raise TimeInError(TimeInError.message)
            case _:
                print('не работает')


    def get_time_delta(self, text_input):
        data = self.get_values()
        time_in = data['time_in']
        time_out = data['time_out']
        delta: timedelta = self.convert(time_out) - self.convert(time_in)
        if delta.days < 0:
            raise ValueError('delta must be >= 0')
        return delta

    def convert_to_my_time_delta(self) -> MyTimeDelta:
        match self.delta.days, self.delta.seconds:
            case d, s if not d:
                 hours = s // 3600
                 minutes = int(s % 3600 / 60)

            case d, s if d:
                hours = (d*24) + (s // 3600)
                minutes = int(s % 3600 / 60)

        return MyTimeDelta(str(hours), str(minutes))

    def get_answer(self):
        delta_in_str = self.convert_to_my_time_delta()
        hours = f'{delta_in_str.hours} ч.'
        minutes = f'{delta_in_str.minutes} мин.'

        in_unit = f'{hours} {minutes}'

        data = self.get_values()
        time_in = data['time_in']
        time_out = data['time_out']
        answer = [
            ['время поступления:', f'{time_in}'],
            ['время перевода:', f'{time_out}'],
            ['всего в отделении:', f'{in_unit}'],
            ['КЭС:', f'{self.get_kes(int(delta_in_str.hours))}']
        ]

        return get_my_table_string(answer, header=False)


