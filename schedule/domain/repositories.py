from shared.domain import Repository
from typing import List
from schedule.domain import entities


class ScheduleRepository(Repository):
    def seen(self) -> List[entities.Schedule]:
        raise NotImplementedError

    def persist(self, schedule: entities.Schedule) -> None:
        raise NotImplementedError

    def find_by_id(self, vendor_id: str) -> entities.Schedule:
        raise NotImplementedError

    def get_appointed_schedules(self) -> List[entities.Schedule]:
        raise NotImplementedError

    def next_identifier(self) -> str:
        raise NotImplementedError
