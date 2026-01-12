import json
import logging
import os
from typing import Dict, List, Optional

import requests
from dotenv import load_dotenv

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def open_json(file_json: str) -> List[Dict]:
    """Функция, которая принимает на вход путь до JSON-файла и возвращает
    список словарей с данными о финансовых транзакциях"""
    logger.info(f"Попытка чтения файла: {file_json}")
    try:
        with open(file_json, "r", encoding="utf-8") as file:
            list_from_file = json.load(file)

        if isinstance(list_from_file, List) and all(isinstance(item, Dict) for item in list_from_file):
            logger.info(f"Успешно загружено {len(list_from_file)} записей.")
            return list_from_file
        else:
            logger.debug(f"Файл '{file_json}' пуст или содержит некорректный формат данных")
            return []

    except FileNotFoundError:
        print(f"Ошибка: Файл не найден по пути '{file_json}'.")
        return []
    except json.JSONDecodeError:
        logger.error(f"Ошибка декодирования JSON в файле: {file_json}")
        return []
    except Exception as e:
        logger.error(f"Ошибка при чтении файла: {file_json}: {e}")
        return []


def external_api(transaction: Dict) -> Optional[float]:
    """Функция, которая принимает на вход транзакцию и
    возвращает сумму транзакции (amount) в рублях"""
    logger.info("Начало обработки транзакции")
    if not isinstance(transaction, dict):
        logger.error("Некорректный формат данных")
        raise TypeError("Некорректный формат данных")

    try:
        amount_val = transaction["operationAmount"]["amount"]
        currency_info = transaction["operationAmount"]["currency"]
        currency_code = currency_info["code"]
    except KeyError:
        logger.warning("Некорректный формат данных: отсутствуют необходимые поля")
        raise TypeError("Некорректный формат данных: отсутствуют необходимые поля")

    try:
        if currency_code == "RUB":
            logger.info(f"Результат: сумма транзакции {round(float(amount_val), 2)} рублей")
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
                logger.info(f"Результат: сумма транзакции {round(float(amount_val), 2)} рублей")
                return round(result.get("result"), 2)
            else:
                logger.error(f"Ошибка API: статус {response.status_code}")
                return None

        else:
            logger.warning(f"Предупреждение: Валюта {currency_code} не поддерживается")
            return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка сети: {e}")
        return None
    except Exception as e:
        logger.error(f"Произошла непредвиденная ошибка: {e}")
        return None
