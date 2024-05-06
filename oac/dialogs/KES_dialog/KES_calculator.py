from datetime import datetime, timedelta
from dataclasses import dataclass

from oac.program_logic.parameters import ParametersForCurrentFunc
from oac.program_logic.my_table import get_my_table_string


@dataclass
class KesCalculator(ParametersForCurrentFunc):
    def __post_init__(self):
        super().__post_init__()
        self.set_current_params('kes_time_count')

    @staticmethod
    def convert(time_str: str) -> datetime:
        time = datetime.strptime(time_str, '%d.%m.%y %H:%M')
        return time

    @staticmethod
    def get_kes(days, hours=0) -> str:
        match days:
            case d if d < 1:
                return '4310 10'
            case d if 1 <= d < 2:
                return '4310 20'
            case d if d >= 2:
                return '4310 30'

    def is_usable_format(self, text_input: str) -> bool:
        # здесь еще нужно за тайм дельту намутить
        try:
            text_input = self.convert(text_input)
        except ValueError:
            return False
        else:
            return True

    def get_answer(self):
        data = self.get_values()
        time_in = data['time_in']
        time_out = data['time_out']
        delta: timedelta = self.convert(time_out) - self.convert(time_in)
        # остановился на отрицательной тайм дельте. этого не может быть!!!!

        days, time = delta.__str__().split(' days, ')
        if int(days) < 0:
            raise ValueError('value must be over zero')

        time = time.split(':')
        days_str = f'{days} д.'
        hours = f'{time[0]} ч.'
        minutes = f'{time[1]} мин.'

        answer = [
            ['время поступления:', f'{time_in}'],
            ['время перевода:', f'{time_out}'],
            ['всего в отделении:', f'{days_str} {hours} {minutes}'],
            ['КЭС:', f'{self.get_kes(int(days))}']
        ]

        return get_my_table_string(answer, header=False)


