# mypy: disable-error-code="no-untyped-def"

from unittest.mock import MagicMock, patch

from src.importers import open_csv_transactions, open_xlsx_transactions


def test_open_csv_not_found():
    # Проверка поведения при отсутствии csv файла.
    assert open_csv_transactions("non_existent.csv") == []


@patch("os.path.exists")
@patch("pandas.read_csv")
def test_open_csv_success(mock_read_csv, mock_exists):
    # Проверка успешного чтения csv.
    mock_exists.return_value = True
    # Создаем фейковый DataFrame и его метод to_dict
    mock_df = MagicMock()
    mock_df.to_dict.return_value = [{"id": 11, "amount": 1000}]
    mock_read_csv.return_value = mock_df

    result = open_csv_transactions("fake.csv")

    assert result == [{"id": 11, "amount": 1000}]
    mock_read_csv.assert_called_once_with("fake.csv", delimiter=";")


@patch("os.path.exists")
@patch("pandas.read_csv")
def test_open_csv_error(mock_read_csv, mock_exists):
    # Проверка обработки ошибки (например, файл поврежден).
    mock_exists.return_value = True
    mock_read_csv.side_effect = Exception("Read error")

    assert open_csv_transactions("broken.csv") == []


def test_open_xlsx_not_found():
    # Проверка поведения при отсутствии XLSX файла.
    assert open_xlsx_transactions("non_existent.xlsx") == []


@patch("os.path.exists")
@patch("pandas.read_excel")
def test_open_xlsx_success(mock_read_excel, mock_exists):
    # Проверка успешного чтения Excel.
    mock_exists.return_value = True
    mock_df = MagicMock()
    mock_df.to_dict.return_value = [{"id": 22, "amount": 2000}]
    mock_read_excel.return_value = mock_df

    result = open_xlsx_transactions("fake.xlsx")

    assert result == [{"id": 22, "amount": 2000}]
    mock_read_excel.assert_called_once_with("fake.xlsx")


@patch("os.path.exists")
@patch("pandas.read_excel")
def test_open_xlsx_empty_file(mock_read_excel, mock_exists):
    # Проверка обработки пустого или некорректного Excel файла.
    mock_exists.return_value = True
    mock_read_excel.side_effect = Exception("Format error")

    assert open_xlsx_transactions("invalid.xlsx") == []
