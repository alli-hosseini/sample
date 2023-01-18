from shared.application.interfaces import Command
from typing import List, Dict, Union


CATEGORY = Dict[str, Union[int | str]]


class CreateSchedule(Command):
    vendor_id: str
    unit: str
    value: int
    categories: List[CATEGORY]


class PublishAppointedSchedules(Command):
    pass
