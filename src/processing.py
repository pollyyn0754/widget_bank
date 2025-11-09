from typing import List, Dict


def filter_by_state(operations: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """Функция, которая принимает список словарей и значение для ключа 'state',
    а возвращает новый список словарей, содержащий только те словари,
    у которых ключ 'state' соответствует указанному значению."""
    filter_operations = [operation for operation in operations if operation.get("state") == state]
    return filter_operations


def sort_by_date(operations: List[Dict], reverse: bool = True) -> List[Dict]:
    """Функция, которая принимает список словарей и необязательный параметр, задающий порядок сортировки
    (по умолчанию — убывание). Функция должна возвращать новый список, отсортированный по дате."""
    sorted_operations = sorted(operations, key=lambda operations: operations["date"], reverse=reverse)
    return sorted_operations
