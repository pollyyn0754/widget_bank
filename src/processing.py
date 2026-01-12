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
        elif "id" not in operation or "state" not in operation or "date" not in operation:
            raise ValueError("Некорректный формат данных")

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
        elif "id" not in operation or "state" not in operation or "date" not in operation:
            raise ValueError("Некорректный формат данных")

    sorted_operations = sorted(operations, key=lambda operations: operations["date"], reverse=reverse)
    return sorted_operations
