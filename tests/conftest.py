# mypy: disable-error-code="no-untyped-def"

import pytest


@pytest.fixture
def long_number():
    return "736541084301358743000"


@pytest.fixture
def short_number():
    return "700792289606361"


@pytest.fixture
def empty_str():
    return ""


@pytest.fixture
def empty_list():
    return None


@pytest.fixture
def invalid_list():
    return [
        {"id": 109876543, "state": "EXECUTED", "dat": "2018-09-10T12:53:10"},
        {"id": 543210987, "stat": "CANCELED", "date": "2018-09-07T02:00:19"},
        {"i_d": 987654321, "state": "PENDING", "date": "2018-09-14T06:47:04"},
        {"id": 210987654, "state": "", "date": "2018-09-15T03:38:00"},
    ]
