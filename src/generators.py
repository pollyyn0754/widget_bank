from typing import List, Iterator


def filter_by_currency(transactions: List, currency_code: str) -> Iterator:
    """Функция, которая принимает на вход список словарей, представляющих транзакции,
    а возвращает итератор, выдающий транзакции, где валюта операции соответствует заданной"""

    if not isinstance(transactions, List):
        raise TypeError("Некорректный формат данных")

    for transaction in transactions:
        if (
            isinstance(transaction, dict)
            and "operationAmount" in transaction
            and "currency" in transaction["operationAmount"]
            and "code" in transaction["operationAmount"]["currency"]
            and transaction["operationAmount"]["currency"]["code"] == currency_code
        ):
            yield transaction


def transaction_descriptions(transactions: List) -> Iterator:
    """Функция, который принимает список словарей с транзакциями и
    возвращает описание каждой операции"""

    if not isinstance(transactions, List):
        raise TypeError("Некорректный формат данных")

    for transaction in transactions:
        if isinstance(transaction, dict) and "description" in transaction:
            yield transaction["description"]


def card_number_generator(start: int, stop: int) -> Iterator:
    """Функция, которая выдает номера банковских карт в заданном диапазоне"""

    if not isinstance(start, int) or not isinstance(stop, int):
        raise TypeError("Некорректный формат введенного диапазона")
    if not (1 <= start <= stop <= 9999999999999999):
        raise ValueError("Некорректный формат введенного диапазона")

    for card_number_int in range(start, stop + 1):
        card_number = f"{card_number_int:016d}"
        yield " ".join([card_number[:4], card_number[4:8], card_number[8:12], card_number[12:]])
