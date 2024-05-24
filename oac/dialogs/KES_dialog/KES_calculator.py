from typing import Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

from oac.program_logic.parameters import ParametersForCurrentFunc
from oac.program_logic.my_table import get_my_table_string


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
    def get_kes(days, hours=0) -> str:
        match days:
            case d if d < 1:
                return '4310 10'
            case d if 1 <= d < 3:
                return '4310 20'
            case d if d >= 3:
                return '4310 30'

    def is_usable_format(self, text_input: str) -> bool:
        # здесь еще нужно за тайм дельту намутить
        try:
            text_input = self.convert(text_input)
            self.delta = self.get_time_delta()

        except ValueError:
            print('дельта не может быть отрицательным')
            return False
        except TypeError:
            print('отсутствуют данные')
            return False
        else:
            return True

    def get_time_delta(self):
        data = self.get_values()
        time_in = data['time_in']
        time_out = data['time_out']
        delta: timedelta = self.convert(time_out) - self.convert(time_in)
        if delta.days < 0:
            raise ValueError('delta must be >= 0')
        return delta

    def get_answer(self):
        data = self.get_values()
        time_in = data['time_in']
        time_out = data['time_out']
        delta_in_str = self.delta.__str__()

        match delta_in_str.split():
            case [d, _, t]:
                days = d
                time = t

            case [t]:
                days = '0'
                time = t

        time = time.split(':')
        days_str = f'{days} д.'
        hours = f'{time[0]} ч.'
        minutes = f'{time[1]} мин.'

        in_unit = f'{days_str} {hours} {minutes}'

        answer = [
            ['время поступления:', f'{time_in}'],
            ['время перевода:', f'{time_out}'],
            ['всего в отделении:', ],
            ['КЭС:', f'{self.get_kes(int(days))}']
        ]

        return get_my_table_string(answer, header=False)


