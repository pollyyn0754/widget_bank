import pytest

from src.widget import mask_account_card, get_date


@pytest.mark.parametrize('acc_card, mask_acc_card', [
    ('Maestro 1596837868705199', 'Maestro 1596 83** **** 5199'),
    ('MasterCard 7158300734726758', 'MasterCard 7158 30** **** 6758'),
    ('Счет 35383033474447895560', 'Счет **5560'),
    ('Visa Classic 6831982476737658', 'Visa Classic 6831 98** **** 7658'),
    ('Visa Platinum 8990922113665229', 'Visa Platinum 8990 92** **** 5229'),
    ('Счет 73654108430135874305', 'Счет **4305')
    ])
def test_mask_account_card(acc_card, mask_acc_card):
    assert mask_account_card(acc_card) == mask_acc_card

def test_mask_acc_card_exception_1(empty_str):
    with pytest.raises(ValueError):
        mask_account_card(empty_str)

def test_mask_acc_card_exceptions():
    with pytest.raises((ValueError, TypeError)):
        mask_account_card('Visa Platinum 700079228960636')
        mask_account_card('Счет 7365410843013587430')
        mask_account_card(123)
        mask_account_card()

def test_get_date():
    assert get_date('2024-03-11T02:26:18.671407') == '11.03.2024'

def test_get_date_exception_1(empty_str):
        with pytest.raises(ValueError):
            get_date(empty_str)

def test_get_date_exceptions():
    with pytest.raises(ValueError):
        get_date('2024-3-11T02:26:18.671407')
        get_date('2024-03-11T02:26:18.67140')
        get_date(123)
        get_date()
