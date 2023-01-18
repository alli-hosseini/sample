from shared.application.interfaces import CommandHandler
from typing import Optional
from .commands import CreateSchedule, PublishAppointedSchedules
from schedule.domain.repositories import ScheduleRepository


class CreateScheduleHandler(CommandHandler):
    def handle(
        self, command: CreateSchedule, repo: Optional[ScheduleRepository]
    ) -> Optional[str]:
        pass


class PublishAppointedHandler(CommandHandler):
    def handle(
        self, command: PublishAppointedSchedules, repo: Optional[ScheduleRepository]
    ) -> Optional[str]:
        pass
