import json
import os
import requests
from dotenv import load_dotenv
from typing import List, Dict, Optional


def open_json(file_json: str) -> List[Dict]:
    """Функция, которая принимает на вход путь до JSON-файла и возвращает
    список словарей с данными о финансовых транзакциях"""
    try:
        with open(file_json, "r", encoding="utf-8") as file:
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


def external_api(transaction: Dict) -> Optional[float]:
    """Функция, которая принимает на вход транзакцию и
    возвращает сумму транзакции (amount) в рублях"""
    if not isinstance(transaction, dict):
        raise TypeError("Некорректный формат данных")

    try:
        amount_val = transaction["operationAmount"]["amount"]
        currency_info = transaction["operationAmount"]["currency"]
        currency_code = currency_info["code"]
    except KeyError:
        raise TypeError("Некорректный формат данных: отсутствуют необходимые поля")

    try:
        if currency_code == "RUB":
            return round(float(amount_val), 2)

        elif currency_code in ["USD", "EUR"]:  # Исправлено EVR на EUR
            load_dotenv()
            api_key = os.getenv("API_KEY")
            url = (
                f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency_code}&amount={amount_val}"
            )

            headers = {"apikey": api_key}
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                result = response.json()
                return round(result.get("result"), 2)
            else:
                print(f"Ошибка API: статус {response.status_code}")
                return None

        else:
            print(f"Предупреждение: Валюта {currency_code} не поддерживается")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети: {e}")
        return None
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        return None
