import os
from typing import Dict, List

import pandas as pd


def open_csv_transactions(filepath: str) -> List[Dict]:
    """Считывает финансовые операции из CSV файла."""
    if not os.path.exists(filepath):
        print(f"Ошибка: Файл не найден по пути {filepath}")
        return []
    try:
        df = pd.read_csv(filepath, delimiter=";").to_dict("records")
        print(f"Успешно прочитано {len(df)} строк из CSV.")
        return df
    except Exception as e:
        print(f"Произошла ошибка при чтении CSV: {e}")
        return []


def open_xlsx_transactions(filepath: str) -> List[Dict]:
    """Считывает финансовые операции из XLSX файла."""
    if not os.path.exists(filepath):
        print(f"Ошибка: Файл не найден по пути {filepath}")
        return []

    try:
        df = pd.read_excel(filepath).to_dict("records")
        print(f"Успешно прочитано {len(df)} строк из XLSX.).")
        return df
    except Exception as e:
        print(f"Произошла ошибка при чтении XLSX: {e}")
        return []
