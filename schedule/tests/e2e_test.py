import datetime
import pytest
from shared.test_utils import marks
from django.test.client import Client
from unittest.mock import patch, MagicMock
from .fake_responses import last_index_categories_response
from schedule.types import CATEGORY
from .fixtures import *
from .fake_responses import schedule_query_response


@pytest.mark.urls("config.urls")
@marks("e2e", "schedule", "django_db")
@patch("src.discovery.modules.index.get_latest_index")
def test_create_schedule(
    mocked_func: MagicMock, client: Client, scheduled_categories: List[CATEGORY]
):
    mocked_func.return_value = last_index_categories_response
    res = client.post(
        "/schedule/create_schedule/",
        {
            "vendor_id": "foo",
            "unit": "hour",
            "value": 2,
            "categories": scheduled_categories,
        },
        "application/json",
    )
    assert res.status_code == 200


@pytest.mark.urls("config.urls")
@marks("e2e", "schedule", "django_db")
@patch("src.schedule.application.handlers.timezone.now")
def test_get_schedule(
    mocked_time: MagicMock,
    client: Client,
    scheduled_categories: List[CATEGORY],
):
    mocked_time.return_value = datetime.datetime(
        2022, 11, 12, 5, 54, 2, 58260, tzinfo=datetime.timezone.utc
    )
    client.post(
        "/schedule/create_schedule/",
        {
            "vendor_id": "mlt",
            "unit": "day",
            "value": 3,
            "categories": scheduled_categories,
        },
        "application/json",
    )
    res = client.get("/schedule/mlt/")

    assert res.status_code == 200
    assert res.json() == schedule_query_response
