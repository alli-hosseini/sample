from pytest import fixture
from schedule.domain import value_objects
from schedule.domain import entities
from schedule.models import ScheduleRepository
from typing import List
from discovery.domain.events import IndexCommitted
from datetime import timedelta
from django.utils import timezone
from schedule.types import CATEGORY
from shared.test_utils import generate_uuid


@fixture
def schedule_configuration() -> value_objects.RescheduleConfig:
    return value_objects.RescheduleConfig(
        next_update_at=timezone.now(),
        delta=value_objects.ScheduleTimeDelta(value=timedelta(days=2)),
    )


@fixture
def updated_schedule_config() -> value_objects.RescheduleConfig:
    return value_objects.RescheduleConfig(
        next_update_at=timezone.now(),
        delta=value_objects.ScheduleTimeDelta(value=timedelta(hours=20)),
    )


@fixture
def schedule(
    schedule_configuration: value_objects.RescheduleConfig,
    vendor: value_objects.Vendor,
) -> entities.Schedule:
    return entities.Schedule(
        vendor=vendor, delta=value_objects.ScheduleTimeDelta(value=timedelta(days=2))
    )


@fixture
def schedule_without_category(
    schedule_configuration: value_objects.RescheduleConfig,
    vendor_without_category: value_objects.Vendor,
) -> entities.Schedule:
    return entities.Schedule(
        vendor=vendor_without_category,
        delta=value_objects.ScheduleTimeDelta(value=timedelta(days=2)),
    )


@fixture
def repo() -> ScheduleRepository:
    return ScheduleRepository()


category2_uuid = generate_uuid()


@fixture
def category2(
    schedule_configuration: value_objects.RescheduleConfig,
) -> value_objects.Category:
    return value_objects.Category(
        identifier=category2_uuid, url="https://bar.com", config=schedule_configuration
    )


@fixture
def categories(category1, category2) -> List[value_objects.Category]:
    return [category1, category2]


@fixture
def vendor(categories) -> value_objects.Vendor:
    return value_objects.Vendor(identifier="digikala", categories=categories)


@fixture
def vendor_without_category() -> value_objects.Vendor:
    return value_objects.Vendor(identifier="foo", categories=None)


@fixture
def index_committed_event() -> IndexCommitted:
    return IndexCommitted(
        vendor_id="vendor_id",
        index_identifier="",
        urls=["https://foo1.com", "https://foo2.com"],
    )


@fixture
def scheduled_categories() -> List[CATEGORY]:
    return [
        {"id": "b37d800e-a8da-49aa-b376-707036314295", "unit": "hour", "value": 10},
        {"id": "b38d800e-a8da-49aa-b376-707036314295", "unit": "hour", "value": 20},
    ]
