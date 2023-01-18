from shared.domain import AggregateRoot
from .events import (
    ScheduleCreated,
    CategoryAdded
)
from .value_objects import (
    Vendor,
    Category,
    ScheduleTimeDelta,
)
from typing import Optional


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

    def add_category(self, category: Category) -> None:
        if category_index := self.find_category_index_by_url(category.url):
            self.vendor.categories[category_index] = category
        else:
            self.vendor.categories.append(category)

        self._record(CategoryAdded(self.vendor.identifier, category.url))

    def find_category_index_by_url(self, url: str) -> Optional[Category]:
        for index, category in enumerate(self.vendor.categories):
            if category.url == url:
                return index
