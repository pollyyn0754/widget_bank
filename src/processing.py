import re
from collections import Counter
from typing import Dict, List


def filter_by_state(operations: List, state: str = "EXECUTED") -> List:
    """Функция, которая принимает список словарей и значение для ключа 'state',
    а возвращает новый список словарей, содержащий только те словари,
    у которых ключ 'state' соответствует указанному значению."""

    if not isinstance(operations, List):
        raise TypeError("Некорректный формат данных")
    for operation in operations:
        if not isinstance(operation, Dict):
            raise TypeError("Некорректный формат данных")

    filter_operations = [operation for operation in operations if operation.get("state") == state]
    return filter_operations


def sort_by_date(operations: List, reverse: bool = True) -> List:
    """Функция, которая принимает список словарей и необязательный параметр, задающий порядок сортировки
    (по умолчанию — убывание). Функция должна возвращать новый список, отсортированный по дате."""

    if not isinstance(operations, List):
        raise TypeError("Некорректный формат данных")
    for operation in operations:
        if not isinstance(operation, Dict):
            raise TypeError("Некорректный формат данных")

    sorted_operations = sorted(operations, key=lambda operations: operations["date"], reverse=reverse)
    return sorted_operations


def process_bank_search(operations: list[dict], search: str) -> list[dict]:
    """Фильтрует транзакции по наличию строки в ключе 'description'."""
    pattern = re.compile(re.escape(search), re.IGNORECASE)

    return [item for item in operations if item.get("description") and pattern.search(item["description"])]


def process_bank_operations(operations: list[dict], categories: list) -> dict:
    """Подсчитывает количество операций в каждой из заданных категорий.
    Категория берется из поля 'description'."""

    descriptions = [op.get("description") for op in operations if "description" in op]
    counts = Counter(descriptions)

    return {category: counts.get(category, 0) for category in categories}
