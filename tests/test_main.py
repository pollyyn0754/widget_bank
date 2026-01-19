# mypy: disable-error-code="no-untyped-def"
from unittest.mock import patch

from main import main


@patch("main.open_json")
@patch("main.filter_by_state")
@patch("main.sort_by_date")
@patch("main.filter_by_currency")
@patch("main.process_bank_search")
@patch("main.mask_account_card")
@patch("main.get_date")
@patch("builtins.input")
def test_main_full_chain(
    mock_input,
    mock_get_date,
    mock_mask,
    mock_search,
    mock_currency,
    mock_sort,
    mock_filter_state,
    mock_open_json,
    capsys,
):
    # Тест полной цепочки: JSON -> Статус -> Сортировка -> Валюта -> Поиск по слову.

    # 1. Имитируем ввод пользователя
    mock_input.side_effect = [
        "1",  # Выбор JSON
        "EXECUTED",  # Статус
        "да",  # Сортировать по дате?
        "по убыванию",  # Порядок сортировки
        "да",  # Только рубли?
        "да",  # Фильтр по слову?
        "Перевод",  # Слово для поиска
    ]

    # 2. Настраиваем возвращаемые значения для каждого этапа
    initial_data = [{"id": 1}]
    mock_open_json.return_value = initial_data

    state_filtered = [{"id": 1, "description": "Перевод"}]
    mock_filter_state.return_value = state_filtered

    sorted_data = state_filtered  # В данном тесте состав не меняем, важен вызов
    mock_sort.return_value = sorted_data

    currency_filtered = sorted_data
    mock_currency.return_value = iter(currency_filtered)  # Фильтр возвращает итератор

    final_data = currency_filtered
    mock_search.return_value = iter(final_data)  # Поиск возвращает итератор

    # Настройка отображения
    mock_get_date.return_value = "01.01.2024"
    mock_mask.return_value = "Visa **1111"

    # 3. Запуск
    main()

    # 4. Проверки вызовов (проверяем, что каждый этап получил данные от предыдущего)
    mock_filter_state.assert_called_once_with(initial_data, "EXECUTED")
    mock_sort.assert_called_once_with(state_filtered, reverse=True)
    mock_currency.assert_called_once_with(sorted_data, "RUB")
    mock_search.assert_called_once_with(sorted_data, "Перевод")

    # Проверка итогового вывода
    captured = capsys.readouterr().out
    assert "Всего банковских операций в выборке: 1" in captured
    assert "01.01.2024" in captured
    assert "Visa **1111" in captured


@patch("main.open_json")
@patch("main.filter_by_state")
@patch("builtins.input")
def test_main_json_flow(mock_input, mock_filter, mock_open_json, capsys):
    # Тест основного сценария: JSON, фильтрация по статусу, без доп. фильтров.

    # Имитируем ввод пользователя по порядку:
    # 1 (JSON), EXECUTED (статус), нет (сортировка), нет (рубли), нет (слово)
    mock_input.side_effect = ["1", "EXECUTED", "нет", "нет", "нет"]

    # Подготавливаем моки данных
    mock_open_json.return_value = [{"id": 1, "state": "EXECUTED", "date": "2023-01-01", "description": "Test"}]
    mock_filter.return_value = [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01", "description": "Test", "to": "Счет 123"}
    ]

    # Запускаем функцию
    with patch("main.mask_account_card", return_value="**1234"):
        with patch("main.get_date", return_value="01.01.2023"):
            main()

    # Проверяем консольный вывод
    captured = capsys.readouterr().out
    assert "Программа: Для обработки выбран JSON-файл." in captured
    assert "Всего банковских операций в выборке: 1" in captured
    assert "01.01.2023 Test" in captured


@patch("builtins.input")
def test_main_invalid_status_retry(mock_input, capsys):
    # Тест повторного ввода при некорректном статусе.

    mock_input.side_effect = [
        "1",  # 1. Выбор JSON
        "INVALID",  # 2. Неверный статус 'INVALID'
        "EXECUTED",  # 3. Верный статус 'EXECUTED'
        "нет",  # 4. Все 'нет'
        "нет",
        "нет",
    ]

    with patch("main.open_json", return_value=[{"id": 1}]):
        with patch("main.filter_by_state", return_value=[]):
            main()

    captured = capsys.readouterr().out
    assert 'Статус операции "INVALID" недоступен.' in captured
    assert 'Операции отфильтрованы по статусу "EXECUTED"' in captured


@patch("main.open_csv_transactions")
@patch("builtins.input")
def test_main_empty_results(mock_input, mock_open_csv, capsys):
    # Тест вывода, когда транзакции не найдены.

    mock_input.side_effect = ["2", "CANCELED", "нет", "нет", "нет"]
    mock_open_csv.return_value = [{"id": 1}]

    # Имитируем, что фильтр вернул пустой список
    with patch("main.filter_by_state", return_value=[]):
        main()

    captured = capsys.readouterr().out
    assert "Не найдено ни одной транзакции, подходящей под ваши условия фильтрации" in captured


@patch("builtins.input")
def test_main_file_not_found_retry(mock_input, capsys):
    # Тест ситуации, когда файл не найден и требуется повторный выбор.

    # Сначала выбираем 1 (файл не найден), потом 2 (успешно)
    mock_input.side_effect = ["1", "2", "EXECUTED", "нет", "нет", "нет"]

    with patch("main.open_json", return_value=[]):  # Пустой список имитирует "не найден"
        with patch("main.open_csv_transactions", return_value=[{"id": 1}]):
            with patch("main.filter_by_state", return_value=[]):
                main()

    captured = capsys.readouterr().out
    assert "Файл не найден" in captured
