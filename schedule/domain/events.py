from shared.domain import DomainEvent
from dataclasses import dataclass


@dataclass
class ScheduleCreated(DomainEvent):
    vendor_id: str


@dataclass
class CategoryAppointed(DomainEvent):
    vendor_id: str
    url: str
