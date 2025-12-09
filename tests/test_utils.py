# mypy: disable-error-code="no-untyped-def"
import pytest
from src.utils import open_json


def test_open_json_result(file_json = "data.operations.json"):
