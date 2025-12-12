# mypy: disable-error-code="no-untyped-def"

import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "acc_card, mask_acc_card",
    [
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ],
)
def test_mask_account_card(acc_card, mask_acc_card):
    assert mask_account_card(acc_card) == mask_acc_card


def test_mask_acc_card_exception_1(empty_str):
    with pytest.raises(ValueError):
        mask_account_card(empty_str)


def test_mask_acc_card_exceptions():
    with pytest.raises(ValueError):
        mask_account_card("Visa Platinum 700079228960636")
        mask_account_card("Счет 7365410843013587430")


@pytest.mark.parametrize("acc_card", [123, [1, 2, 3], None])
def test_mask_account_card_exceptions_2(acc_card):
    with pytest.raises(TypeError):
        mask_account_card(acc_card)


@pytest.mark.parametrize(
    "date_inf, date",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2019-07-03T18:35:29.512364", "03.07.2019"),
        ("2018-06-30T02:08:58.425572", "30.06.2018"),
    ],
)
def test_get_date(date_inf, date):
    assert get_date(date_inf) == date


def test_get_date_exception_1(empty_str):
    with pytest.raises(ValueError):
        get_date(empty_str)


def test_get_date_exceptions():
    with pytest.raises(ValueError):
        get_date("2024-3-11T02:26:18.671407")
        get_date("2024-03-11T02:26:18.67140")
        get_date("2024-08-11T02:26:18.6714070")


@pytest.mark.parametrize("date_infs", [123, [1, 2, 3], None])
def test_get_date_exceptions_exceptions_2(date_infs):
    with pytest.raises(TypeError):
        get_date(date_infs)
