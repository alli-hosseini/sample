from shared.application.interfaces import Query
from dataclasses import dataclass


@dataclass
class ScheduleQuery(Query):
    vendor_id: str
