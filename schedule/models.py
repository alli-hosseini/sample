import uuid
from django.db import models
from django.db.models import Prefetch
from schedule.domain import repositories
from typing import List
from schedule.domain import entities
from schedule.domain import value_objects
from django.utils import timezone


class Schedule(models.Model):
    vendor_id = models.CharField(max_length=250, unique=True)
    value = models.DurationField()

    def to_domain(self) -> entities.Schedule:
        categories = []
        if hasattr(self, "_prefetched_objects_cache"):
            categories = [
                c.to_domain()
                for c in self._prefetched_objects_cache.get("category_set", [])
            ]
        return entities.Schedule(
            vendor=value_objects.Vendor(
                identifier=self.vendor_id, categories=categories
            ),
            delta=value_objects.ScheduleTimeDelta(value=self.value),
        )


class Category(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=255, primary_key=True)
    url = models.CharField(max_length=2048)
    value = models.DurationField(null=True)
    next_update_at = models.DateTimeField(null=True)

    def to_domain(self) -> value_objects.Category:
        return value_objects.Category(
            identifier=self.identifier,
            url=self.url,
            config=value_objects.RescheduleConfig(
                next_update_at=self.next_update_at,
                delta=value_objects.ScheduleTimeDelta(value=self.value),
            )
            if self.value
            else None,
        )


class ScheduleRepository(repositories.ScheduleRepository):
    def __init__(self):
        self._seen = []

    def seen(self) -> List[entities.Schedule]:
        return self._seen

    def persist(self, schedule: entities.Schedule) -> None:
        self._create_schedule(schedule)

    def find_by_id(self, vendor_id: str) -> entities.Schedule:
        schedule = Schedule.objects.filter(vendor_id=vendor_id).prefetch_related(
            "category_set"
        )
        return schedule.first().to_domain() if schedule else None

    def next_identifier(self) -> str:
        return str(uuid.uuid4())

    def get_appointed_schedules(self) -> List[entities.Schedule]:
        return list(
            map(
                lambda schedule: schedule.to_domain(),
                Schedule.objects.prefetch_related(
                    Prefetch(
                        "category_set",
                        queryset=Category.objects.filter(
                            next_update_at__range=(
                                timezone.now() - timezone.timedelta(minutes=1),
                                timezone.now() + timezone.timedelta(minutes=1),
                            ),
                        ),
                    )
                ),
            )
        )

    # helper functions #
    @staticmethod
    def _create_schedule(schedule: entities.Schedule) -> None:
        s = Schedule.objects.create(
            vendor_id=schedule.vendor.identifier,
            value=schedule.delta.value,
        )
        categories = []
        if schedule.vendor.categories:
            for category in schedule.vendor.categories:
                categories.append(
                    Category(
                        schedule=s,
                        identifier=category.identifier,
                        url=category.url,
                        value=category.config.delta.value,
                        next_update_at=category.config.next_update_at,
                    )
                )
        Category.objects.bulk_create(categories)
