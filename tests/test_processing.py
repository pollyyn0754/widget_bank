# mypy: disable-error-code="no-untyped-def"

import pytest


from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize(
    "operations, sorted_operations, state_value",
    [
        (
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
            "EXECUTED",
        ),
        (
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
            [
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
            ],
            "CANCELED",
        ),
        (
            [
                {"id": 939719570, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 142269225, "state": "PENDING", "date": "2018-09-10T15:26:07.728955"},
                {"id": 615064591, "state": "EXECUTED", "date": "2018-09-08T18:25:31.954751"},
            ],
            [{"id": 615064591, "state": "EXECUTED", "date": "2018-09-08T18:25:31.954751"}],
            "",
        ),
    ],
)
def test_filter_by_state(operations, sorted_operations, state_value):
    filter_by_state(operations, state=state_value) == sorted_operations


def test_filter_by_state_empty_list(empty_list):
    assert filter_by_state(empty_list) == []


def test_filter_by_state_exception_2(invalid_list):
    with pytest.raises(ValueError):
        filter_by_state(invalid_list)


@pytest.mark.parametrize(
    "operations, date_value",
    [
        (
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            [
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        ),
        (
            [
                {"id": 678901234, "state": "PENDING", "date": "2018-09-11T23:59:02"},
                {"id": 123456789, "state": "CANCELED", "date": "2018-09-05T09:33:48"},
                {"id": 567890123, "state": "EXECUTED", "date": "2018-09-04T16:22:15"},
            ],
            [
                {"id": 678901234, "state": "PENDING", "date": "2018-09-11T23:59:02"},
                {"id": 123456789, "state": "CANCELED", "date": "2018-09-05T09:33:48"},
                {"id": 567890123, "state": "EXECUTED", "date": "2018-09-04T16:22:15"},
            ],
        ),
    ],
)
def test_sort_by_date(operations, date_value):
    sort_by_date(operations) == date_value


def test_sort_by_date_empty_list(empty_list):
    assert sort_by_date(empty_list) == []


def test_sort_by_date_exception_2(invalid_list):
    with pytest.raises(ValueError):
        sort_by_date(invalid_list)
