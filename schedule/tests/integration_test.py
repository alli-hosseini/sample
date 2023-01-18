from src.seedwork.test_utils import marks
from src.schedule.domain.entities import Schedule
from src.schedule import models
from .fixtures import *


@marks("integration", "schedule", "django_db")
def test_persist(schedule: Schedule, repo: models.ScheduleRepository):
    category = schedule.vendor.categories[0]
    repo.persist(schedule)
    persisted_schedule = repo.find_by_id(schedule.vendor.identifier)
    persisted_category = schedule.vendor.categories[0]

    assert persisted_schedule.vendor.identifier == schedule.vendor.identifier
    assert persisted_schedule.delta.value == schedule.delta.value
    assert persisted_category.identifier == category.identifier
    assert persisted_category.url == category.url
    assert persisted_category.config.next_update_at == category.config.next_update_at
    assert persisted_category.config.delta.value == category.config.delta.value


@marks("integration", "schedule", "django_db")
def test_persist_idempotency(
    schedule: Schedule,
    repo: models.ScheduleRepository,
):
    repo.persist(schedule)
    repo.persist(schedule)
    persisted_schedule = repo.find_by_id(schedule.vendor.identifier)

    assert len(persisted_schedule.vendor.categories) == len(schedule.vendor.categories)


@marks("integration", "schedule", "django_db")
def test_update_schedule(schedule: entities.Schedule, repo: models.ScheduleRepository):
    repo.persist(schedule)
    schedule.delta.value = updated_delta = timezone.timedelta(days=4)
    repo.persist(schedule)

    persisted_schedule = repo.find_by_id(schedule.vendor.identifier)
    assert persisted_schedule.delta.value == updated_delta
    assert len(persisted_schedule.vendor.categories) == len(schedule.vendor.categories)


@marks("integration", "schedule", "django_db")
def test_update_category(
    schedule: entities.Schedule,
    repo: models.ScheduleRepository,
):
    repo.persist(schedule)
    category = schedule.vendor.categories[0]
    category.config.delta.value = updated_config = timezone.timedelta(days=1)
    repo.persist(schedule)
    persisted_schedule = repo.find_by_id(schedule.vendor.identifier)

    assert persisted_schedule.vendor.categories[0].config.delta.value == updated_config
    assert len(persisted_schedule.vendor.categories) == len(schedule.vendor.categories)


@marks("integration", "schedule", "django_db")
def test_get_appointed_schedules(
    schedule: entities.Schedule, repo: models.ScheduleRepository
):
    schedule.vendor.categories = []
    five_minutes_later, five_minutes_ago = (
        timezone.now() - timezone.timedelta(minutes=5),
        timezone.now() + timezone.timedelta(minutes=5),
    )
    schedule.add_category(
        value_objects.Category(
            generate_uuid(),
            "url",
            value_objects.RescheduleConfig(
                next_update_at=five_minutes_ago,
                delta=value_objects.ScheduleTimeDelta(
                    value=timezone.timedelta(hours=10)
                ),
            ),
        )
    )
    schedule.add_category(
        value_objects.Category(
            generate_uuid(),
            "url_2",
            value_objects.RescheduleConfig(
                next_update_at=five_minutes_later,
                delta=value_objects.ScheduleTimeDelta(
                    value=timezone.timedelta(hours=10)
                ),
            ),
        )
    )
    schedule.add_category(
        value_objects.Category(
            generate_uuid(),
            "url_3",
            value_objects.RescheduleConfig(
                next_update_at=timezone.now(),
                delta=value_objects.ScheduleTimeDelta(
                    value=timezone.timedelta(hours=10)
                ),
            ),
        )
    )
    repo.persist(schedule)
    categories = repo.get_appointed_schedules()[0].vendor.categories

    assert len(categories) == 1
    assert categories[0].url == "url_3"
