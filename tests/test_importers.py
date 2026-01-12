# mypy: disable-error-code="no-untyped-def"

from unittest.mock import patch

import pandas as pd

from src.importers import read_csv_transactions, read_xlsx_transactions


@patch("os.path.exists")
@patch("pandas.read_csv")
def test_read_csv_transactions_success(mock_read_csv, mock_exists):
    """Тест успешного чтения CSV."""
    mock_exists.return_value = True
    # Создаем фейковый DataFrame
    mock_df = pd.DataFrame({"id": [11, 22], "amount": [1000, 2000]})
    mock_read_csv.return_value = mock_df

    result = read_csv_transactions("test.csv")

    assert result.shape == (2, 2)
    assert len(result) == 2
    assert list(result.columns) == ["id", "amount"]
    mock_read_csv.assert_called_once_with("test.csv")


@patch("os.path.exists")
@patch("pandas.read_excel")
def test_read_xlsx_transactions_success(mock_read_excel, mock_exists):
    """Тест успешного чтения XLSX."""
    mock_exists.return_value = True
    mock_df = pd.DataFrame({"id": [1], "amount": [1000]})
    mock_read_excel.return_value = mock_df

    result = read_xlsx_transactions("test.xlsx")

    assert result.shape == (1, 2)
    assert not result.empty
    assert result.iloc[0]["amount"] == 1000
    mock_read_excel.assert_called_once()


@patch("os.path.exists")
def test_read_file_not_found(mock_exists):
    """Тест поведения, если файл отсутствует."""
    mock_exists.return_value = False

    # Проверяем для CSV
    result_csv = read_csv_transactions("missing.csv")
    # Проверяем для XLSX
    result_xlsx = read_xlsx_transactions("missing.xlsx")

    assert result_csv.empty
    assert result_xlsx.empty
    assert isinstance(result_csv, pd.DataFrame)


@patch("os.path.exists")
@patch("pandas.read_csv")
def test_read_csv_handle_exception(mock_read_csv, mock_exists):
    """Тест обработки исключения при чтении поврежденного CSV."""
    mock_exists.return_value = True
    mock_read_csv.side_effect = Exception("Pandas error")

    result = read_csv_transactions("corrupt.csv")

    assert result.empty
    mock_read_csv.assert_called_once()
