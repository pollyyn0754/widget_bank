# mypy: disable-error-code="no-untyped-def"
from unittest.mock import MagicMock, patch

import pytest
import requests

from src.utils import external_api, open_json


def test_open_json_valid(mock_create_json):
    data = [{"amount": 100, "currency": "RUB"}, {"amount": 200, "currency": "USD"}]
    path = mock_create_json("valid.json", data)
    assert open_json(path) == data
    assert len(open_json(path)) == 2


def test_open_json_empty_list(mock_create_json):
    path = mock_create_json("empty.json", [])
    assert open_json(path) == []
    assert len(open_json(path)) == 0


def test_open_json_invalid_structure(mock_create_json):
    data = {"key": "value"}
    path = mock_create_json("wrong_struct.json", data)
    assert open_json(path) == []


def test_open_json_invalid_items(mock_create_json):
    data = [{"id": 1}, "not_a_dict"]
    path = mock_create_json("wrong_items.json", data)
    assert open_json(path) == []


def test_open_json_decode_error(mock_create_json):
    path = mock_create_json("broken.json", "{'invalid': json}")
    assert open_json(path) == []


def test_open_json_empty_file(mock_create_json):
    path = mock_create_json("nothing.json", "")
    assert open_json(path) == []


def test_open_json_file_not_found():
    assert open_json("non_existent_file.json") == []


def test_external_api_rub(transaction_rub):
    assert external_api(transaction_rub) == 100.5


@patch("requests.get")
@patch("os.getenv")
def test_external_api_usd_success(mock_getenv, mock_get, transaction_usd):
    mock_getenv.return_value = "fake_api_key"

    # Имитируем ответ от сервера
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 7500.0}
    mock_get.return_value = mock_response

    result = external_api(transaction_usd)

    assert result == 7500.00
    mock_get.assert_called_once()


def test_external_api_invalid_structure():
    invalid_data = {"something": "else"}
    with pytest.raises(TypeError, match="Некорректный формат данных"):
        external_api(invalid_data)


@patch("requests.get")
@patch("os.getenv")
def test_external_api_http_error(mock_getenv, mock_get, transaction_usd):
    mock_getenv.return_value = "fake_api_key"

    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    result = external_api(transaction_usd)
    assert result is None


@patch("requests.get")
def test_external_api_network_error(mock_get, transaction_usd):
    mock_get.side_effect = requests.exceptions.RequestException()

    result = external_api(transaction_usd)
    assert result is None
