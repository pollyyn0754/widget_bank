import os
from typing import Union

import pandas as pd


def read_csv_transactions(filepath: str) -> pd.DataFrame:
    """Считывает финансовые операции из CSV файла."""
    if not os.path.exists(filepath):
        print(f"Ошибка: Файл не найден по пути {filepath}")
        return pd.DataFrame()

    try:
        df = pd.read_csv(filepath)
        print(f"Успешно прочитано {len(df)} строк из CSV.")
        return df
    except Exception as e:
        print(f"Произошла ошибка при чтении CSV: {e}")
        return pd.DataFrame()


def read_xlsx_transactions(filepath: str, sheet_name: Union[str, int] = 0) -> pd.DataFrame:
    """Считывает финансовые операции из XLSX файла."""
    if not os.path.exists(filepath):
        print(f"Ошибка: Файл не найден по пути {filepath}")
        return pd.DataFrame()

    try:
        df = pd.read_excel(filepath, sheet_name=sheet_name)
        print(f"Успешно прочитано {len(df)} строк из XLSX (лист: {sheet_name}).")
        return df
    except Exception as e:
        print(f"Произошла ошибка при чтении XLSX: {e}")
        return pd.DataFrame()
