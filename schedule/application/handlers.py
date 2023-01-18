from shared.application.interfaces import CommandHandler
from typing import Optional
from .commands import CreateSchedule, PublishAppointedSchedules
from schedule.domain.repositories import ScheduleRepository
from schedule.domain.value_objects import Vendor
from schedule.domain.entities import Schedule
from schedule.domain.value_objects import ScheduleTimeDelta
from django.utils import timezone


class CreateScheduleHandler(CommandHandler):
    def handle(
        self, command: CreateSchedule, repo: ScheduleRepository
    ) -> Optional[str]:
        schedule = Schedule(
            vendor=Vendor(identifier=command.vendor_id, categories=[]),
            delta=ScheduleTimeDelta(value=timezone.timedelta(hours=2))
            )
        repo.persist(schedule)


class PublishAppointedHandler(CommandHandler):
    def handle(
        self, command: PublishAppointedSchedules, repo: ScheduleRepository
    ) -> Optional[str]:
        pass
