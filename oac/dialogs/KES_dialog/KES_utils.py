from dataclasses import dataclass
from typing import Optional
from datetime import timedelta


@dataclass
class MyTimeDelta:
    delta: Optional[timedelta] = None
    hours: int = 0
    minutes: int = 0

    def normalize(self) -> object:
        match self.delta.days, self.delta.seconds:
            case d, s if not d:
                self.hours = s // 3600
                self.minutes = int(s % 3600 / 60)

            case d, s if d:
                self.hours = (d * 24) + (s // 3600)
                self.minutes = int(s % 3600 / 60)

        return self


class TimeOutError(Exception):
    message = 'время выбытия должно быть больше, чем время приема'


class TimeInError(Exception):
    message = 'время приема должно быть меньше, чем время выбытия'


