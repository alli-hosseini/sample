from shared.application.interfaces import QueryHandler
from . import models
from .application.queries import ScheduleQuery
from shared.application.interfaces import NoQueryResultException
from django.utils import timezone


class ScheduleQueryHandler(QueryHandler):
    def handle(self, query: ScheduleQuery):
        schedule = models.Schedule.objects.filter(vendor_id=query.vendor_id)
        if not schedule:
            raise NoQueryResultException("schedule not found")
        schedule = schedule.first()
        categories = models.Category.objects.filter(schedule=schedule)

        return {
            "vendor_id": schedule.vendor_id,
            "unit": self.timedelta_to_unit(schedule.value),
            "value": self.timedelta_to_value(schedule.value),
            "categories": [
                {
                    "id": category.identifier,
                    "url": category.url,
                    "unit": self.timedelta_to_unit(category.value),
                    "value": self.timedelta_to_value(category.value),
                    "next_update_at": int(category.next_update_at.strftime("%s")),
                }
                for category in categories
            ],
        }

    @staticmethod
    def timedelta_to_unit(timedelta: timezone.timedelta) -> str:
        return "day" if timedelta.days else "hour"

    @staticmethod
    def timedelta_to_value(timedelta: timezone.timedelta) -> int:
        return timedelta.days if timedelta.days else timedelta.seconds // 3600
