import os

from src.generators import filter_by_currency
from src.importers import open_csv_transactions, open_xlsx_transactions
from src.processing import filter_by_state, process_bank_search, sort_by_date
from src.utils import open_json
from src.widget import get_date, mask_account_card


def main() -> None:
    """Функция, которая отвечает за основную логику проекта и связывает функциональности между собой."""

    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    while True:
        choice_file = ""
        while choice_file not in ["1", "2", "3"]:
            print("Выберите необходимый пункт меню:")
            print("1. Получить информацию о транзакциях из JSON-файла")
            print("2. Получить информацию о транзакциях из CSV-файла")
            print("3. Получить информацию о транзакциях из XLSX-файла")
            choice_file = input("Пользователь: ")
            if choice_file not in ["1", "2", "3"]:
                print("Неверный выбор.")
        operations = []
        if choice_file == "1":
            print("Программа: Для обработки выбран JSON-файл.")
            operations = open_json(os.path.join("data", "operations.json"))
        elif choice_file == "2":
            print("Программа: Для обработки выбран CSV-файл.")
            operations = open_csv_transactions(os.path.join("data", "transactions.csv"))
        elif choice_file == "3":
            print("Программа: Для обработки выбран XLSX-файл.")
            operations = open_xlsx_transactions(os.path.join("data", "transactions_excel.xlsx"))

        if operations == []:
            print("Файл не найден")
        else:
            break

    # Фильтрация по статусу
    while True:
        status = input(
            "\nПрограмма: Введите статус, по которому необходимо выполнить фильтрацию.\n"
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\nПользователь: "
        ).upper()
        if status in ["EXECUTED", "CANCELED", "PENDING"]:
            transactions = filter_by_state(operations, status)
            print(f'Программа: Операции отфильтрованы по статусу "{status}"')
            break
        else:
            print(f'Программа: Статус операции "{status}" недоступен.')

    # Сортировка по дате
    if input("\nПрограмма: Отсортировать операции по дате? Да/Нет\nПользователь: ").lower() == "да":
        order = input("Программа: Отсортировать по возрастанию или по убыванию?\nПользователь: ").lower()
        reverse = True if order == "по убыванию" else False
        transactions = sort_by_date(transactions, reverse=reverse)

    # Фильтрация по валюте
    if input("\nПрограмма: Выводить только рублевые транзакции? Да/Нет\nПользователь: ").lower() == "да":
        transactions = list(filter_by_currency(transactions, "RUB"))

    # Фильтрация по слову
    if (
        input(
            "\nПрограмма: Отфильтровать список транзакций по определенному слову в описании? " "Да/Нет\nПользователь: "
        ).lower()
        == "да"
    ):
        word = input("Введите слово для поиска: ")
        transactions = list(process_bank_search(transactions, word))

    if transactions == []:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(
            f"Программа: Распечатываю итоговый список транзакций...\n"
            f"Программа: Всего банковских операций в выборке: {len(transactions)}\n"
        )
        for op in transactions:

            # Форматирование даты
            date = get_date(op.get("date"))
            desc = op.get("description")

            # Маскирование отправителя и получателя
            from_masked = mask_account_card(op.get("from")) if "from" in op and str(op.get("from")) != "nan" else ""
            to_masked = mask_account_card(op.get("to"))

            transfer_line = (
                f"{from_masked} -> {to_masked}" if "from" in op and str(op.get("from")) != "nan" else f"{to_masked}"
            )

            # Сумма (учитываем разную структуру JSON и CSV/XLSX)
            amount = (
                op.get("operationAmount", {}).get("amount")
                if isinstance(op.get("operationAmount"), dict)
                else op.get("amount")
            )
            currency = (
                op.get("operationAmount", {}).get("currency", {}).get("name")
                if isinstance(op.get("operationAmount"), dict)
                else op.get("currency_name")
            )

            print(f"{date} {desc}\n{transfer_line}\nСумма: {amount} {currency}\n")


if __name__ == "__main__":
    main()
