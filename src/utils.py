import json
from typing import List, Dict


def open_json(file_json: str) -> List:
    """Функция, которая принимает на вход путь до JSON-файла и возвращает
    список словарей с данными о финансовых транзакциях"""
    try:
        with open(file_json, 'r', encoding='utf-8') as file:
            list_from_file = json.load(file)

        if isinstance(list_from_file, List) and all(isinstance(item, Dict) for item in list_from_file):
            return list_from_file
        else:
            return []

    except FileNotFoundError:
        print(f"Ошибка: Файл не найден по пути '{file_json}'.")
        return []

    except json.JSONDecodeError:
        print(f"Ошибка декодирования JSON: Файл '{file_json}' пуст или содержит некорректный JSON.")
        return []

    except Exception as e:
        print(f"Произошла непредвиденная ошибка при чтении файла '{file_json}': {e}")
        return []

