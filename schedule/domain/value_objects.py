from shared.domain import ValueException
from typing import List, Optional
from django.utils.timezone import timedelta, datetime


class ScheduleTimeDelta:
    def __init__(self, value: timedelta):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value: timedelta):
        if new_value < timedelta(hours=2):
            raise ValueException("delta should be more than 2 hours")
        self._value = new_value

    @staticmethod
    def from_string(unit: str, value: int) -> "ScheduleTimeDelta":
        return ScheduleTimeDelta(timedelta(**{unit + "s": value}))


class RescheduleConfig:
    def __init__(self, next_update_at: datetime, delta: ScheduleTimeDelta):
        self.next_update_at = next_update_at
        self.delta = delta


class Category:
    def __init__(self, identifier: str, url: str, config: Optional[RescheduleConfig]):
        self.identifier = identifier
        self.url = url
        self.config = config


class Vendor:
    def __init__(self, identifier: str, categories: Optional[List[Category]]):
        self.identifier = identifier
        self.categories = [] if not categories else categories
