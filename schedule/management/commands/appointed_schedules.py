from django.core.management.base import BaseCommand
from schedule.application.commands import PublishAppointedSchedules
from shared.application.bus import bus


class Command(BaseCommand):
    help = "This command will return all appointed schedules"

    def handle(self, *args, **options):
        command = PublishAppointedSchedules()
        bus.handle(command)
