# mypy: disable-error-code="no-untyped-def"
import pytest
from time import ctime
from src.decorators import log


def test_log_result():
    @log()
    def add(a, b):
        return a + b

    result = add(1, 1)
    assert result == 2


def test_log_existent():
    @log(filename="mylog.txt")
    def example_function():
        raise ValueError("Ошибка")

    with pytest.raises(Exception):
        example_function()


def test_log_consol(capsys):
    @log()
    def hello_world():
        return "Hello, world!"

    hello_world()
    captured = capsys.readouterr()
    log_info = (
        f"{ctime()} Начало выполнения функции 'hello_world'. Параметры: "
        "args=(), kwargs={}\n"
        f"{ctime()} Функция 'hello_world' успешно завершена. Результат: "
        "Hello, world!.\n\n"
    )
    assert captured.out == log_info


def test_log_file():
    @log(filename="mylog.txt")
    def subtract(a, b):
        return a - b

    with open("mylog.txt", "w", encoding="utf-8") as file:
        pass
    subtract(10, 5)
    with open("mylog.txt", "r", encoding="utf-8") as file:
        file_message = file.read()
    assert (
        file_message == f"{ctime()} Начало выполнения функции 'subtract'. Параметры: "
        "args=(10, 5), kwargs={}\n"
        f"{ctime()} Функция 'subtract' успешно завершена. Результат: 5.\n"
    )
