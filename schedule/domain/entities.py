from shared.domain import AggregateRoot
from .events import (
    ScheduleCreated,
)
from .value_objects import (
    Vendor,
    Category,
    ScheduleTimeDelta,
)


class Schedule(AggregateRoot):
    def __init__(self, vendor: Vendor, delta: ScheduleTimeDelta):
        super(Schedule, self).__init__()
        self.vendor = vendor
        self.delta = delta

    @classmethod
    def create(cls, vendor: Vendor, delta: ScheduleTimeDelta) -> "Schedule":
        s = cls(vendor, delta)
        s._record(ScheduleCreated(vendor_id=s.vendor.identifier))
        return s

    def reschedule_category(self, category: Category) -> None:
        pass

    def add_category(self, category: Category) -> None:
        pass

    def find_category_by_url(self, url: str) -> int:
        pass
