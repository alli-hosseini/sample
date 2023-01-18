from shared.test_utils import marks
from .fixtures import *
from schedule.domain.events import CategoryAppointed, ScheduleCreated


@marks("unit", "schedule")
def test_create_schedule(
    vendor: value_objects.Vendor, schedule_configuration: value_objects.RescheduleConfig
):
    s = entities.Schedule.create(vendor, schedule_configuration.delta)
    assert isinstance(vendor, entities.Vendor)
    assert isinstance(s.vendor.categories.pop(), value_objects.Category)
    assert isinstance(s.delta, value_objects.ScheduleTimeDelta)
    assert isinstance(s._events.pop(), ScheduleCreated)


@marks("unit", "schedule")
def test_schedule_category_using_global_config(schedule: entities.Schedule):
    schedule.vendor.categories = []
    schedule.add_category(
        category := value_objects.Category(
            generate_uuid(),
            "url",
            None,
        )
    )
    schedule.reschedule_category(category=category)
    assert isinstance(category.config, value_objects.RescheduleConfig)
    assert category.config.delta == schedule.delta
    assert isinstance(schedule._events.pop(), CategoryAppointed)


@marks("unit", "schedule")
def test_schedule_category(schedule: entities.Schedule):
    schedule.vendor.categories = []
    now = timezone.now()
    schedule.add_category(
        category := value_objects.Category(
            generate_uuid(),
            "url",
            value_objects.RescheduleConfig(
                next_update_at=now,
                delta=value_objects.ScheduleTimeDelta(value=timedelta(hours=10)),
            ),
        )
    )

    schedule.reschedule_category(category=category)

    after_reschedule = category.config.next_update_at
    before_reschedule = timezone.now() + category.config.delta.value

    assert before_reschedule.date() == after_reschedule.date()
    assert before_reschedule.strftime("%H:%M") == after_reschedule.strftime("%H:%M")
    assert isinstance(schedule._events.pop(), CategoryAppointed)
