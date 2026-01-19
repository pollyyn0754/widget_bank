# mypy: disable-error-code="no-untyped-def"


import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


def test_filter_by_currency_usd(sample_transactions):
    currency_code = "USD"
    result_iterator = filter_by_currency(sample_transactions, currency_code)
    result_list = list(result_iterator)

    assert len(result_list) == 3
    for transaction in result_list:
        assert transaction["operationAmount"]["currency"]["code"] == currency_code
    assert result_list[0]["id"] == 939719570
    assert result_list[1]["id"] == 142264268
    assert result_list[2]["id"] == 895315941


def test_filter_by_currency_rub(sample_transactions):
    currency_code = "RUB"
    result_iterator = filter_by_currency(sample_transactions, currency_code)
    result_list = list(result_iterator)

    assert len(result_list) == 2
    for transaction in result_list:
        assert transaction["operationAmount"]["currency"]["code"] == currency_code
    assert result_list[0]["id"] == 873106923
    assert result_list[1]["id"] == 594226727


def test_filter_by_currency_non_existent(sample_transactions):
    currency_code = "EUR"
    result_iterator = filter_by_currency(sample_transactions, currency_code)
    result_list = list(result_iterator)

    assert len(result_list) == 0
    assert result_list == []


def test_filter_by_currency_empty_list(empty_list):
    currency_code = "USD"
    result_iterator = filter_by_currency(empty_list, currency_code)
    result_list = list(result_iterator)

    assert result_list == []


@pytest.mark.parametrize("test_list", [123, "123", None])
def test_filter_by_currency_exceptions(test_list):
    with pytest.raises(TypeError):
        filter_by_currency(test_list)


def test_filter_by_currency_invalid(invalid_list):
    currency_code = "USD"
    result_iterator = filter_by_currency(invalid_list, currency_code)
    result_list = list(result_iterator)

    assert len(result_list) == 0


def test_transaction_descriptions(sample_transactions):
    result_iterator = transaction_descriptions(sample_transactions)
    result_list = list(result_iterator)

    assert len(result_list) == 5
    assert result_list == [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]


def test_transaction_descriptions_empty_list(empty_list):
    result_iterator = transaction_descriptions(empty_list)
    result_list = list(result_iterator)

    assert result_list == []


@pytest.mark.parametrize("test_list", [123, "123", None])
def test_transaction_descriptions_exceptions(test_list):
    with pytest.raises(TypeError):
        list(transaction_descriptions(test_list))


def test_transaction_descriptions_invalid(invalid_list):
    result_iterator = transaction_descriptions(invalid_list)
    result_list = list(result_iterator)

    assert len(result_list) == 0


def test_card_number_generator():
    result = list(card_number_generator(12356, 12360))

    assert len(result) == 5
    assert result == [
        "0000 0000 0001 2356",
        "0000 0000 0001 2357",
        "0000 0000 0001 2358",
        "0000 0000 0001 2359",
        "0000 0000 0001 2360",
    ]


@pytest.mark.parametrize("start, stop", [(3000, 2000), (0, 100), (1, 100000000000000000)])
def test_card_number_generator_exceptions(start, stop):
    with pytest.raises(ValueError):
        list(card_number_generator(start, stop))


@pytest.mark.parametrize("start, stop", [("2", 2), (1, 10.5)])
def test_card_number_generator_exceptions_1(start, stop):
    with pytest.raises(TypeError):
        list(card_number_generator(start, stop))
