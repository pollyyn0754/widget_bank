# mypy: disable-error-code="no-untyped-def"


import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "card_numb, mask_cart_numb",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("5999414228426353", "5999 41** **** 6353"),
        ("8990922113665229", "8990 92** **** 5229"),
    ],
)
def test_get_mask_card_number(card_numb, mask_cart_numb):
    assert get_mask_card_number(card_numb) == mask_cart_numb


def test_get_mask_card_exception_1(long_number):
    with pytest.raises(ValueError):
        get_mask_card_number(long_number)


def test_get_mask_card_exception_2(short_number):
    with pytest.raises(ValueError):
        get_mask_card_number(short_number)


def test_get_mask_card_exception_3(empty_str):
    with pytest.raises(ValueError):
        get_mask_card_number(empty_str)


def test_get_mask_card_number_exceptions():
    with pytest.raises((ValueError, TypeError)):
        get_mask_card_number("700079228960636L")
        get_mask_card_number(123)


def test_get_mask_account():
    assert get_mask_account("73654108430135874305") == "**4305"


def test_get_mask_account_exception_1(long_number):
    with pytest.raises(ValueError):
        get_mask_account(long_number)


def test_get_mask_account_exception_2(short_number):
    with pytest.raises(ValueError):
        get_mask_account(short_number)


def test_get_mask_account_exception_3(empty_str):
    with pytest.raises(ValueError):
        get_mask_account(empty_str)


def test_get_mask_account_exceptions():
    with pytest.raises((ValueError, TypeError)):
        get_mask_account("7365410843013587430L")
        get_mask_account(123)
