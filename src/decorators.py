from functools import wraps
from time import ctime
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """Декоратор, который автоматически логирует начало и конец выполнения функции,
    а также ее результаты или возникшие ошибки. Принимает необязательный аргумент filename,
    который определяет, куда будут записываться логи"""

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = ctime()
            try:
                result = func(*args, **kwargs)
                stop_time = ctime()
                log_info = (
                    f"{start_time} Начало выполнения функции '{func.__name__}'. "
                    f"Параметры: args={args}, kwargs={kwargs}\n"
                    f"{stop_time} Функция '{func.__name__}' успешно завершена. Результат: {result}."
                )
                return result
            except Exception as e:
                log_info = (
                    f"{start_time} Начало выполнения функции '{func.__name__}'. "
                    f"Ошибка при выполнении функции '{func.__name__}'. "
                    f"Тип ошибки: {type(e).__name__}. \n"
                    f"Параметры: args={args}, kwargs={kwargs}"
                )
                raise
            finally:
                if filename:
                    with open(filename, "a", encoding="utf-8") as file:
                        file.write(log_info)
                else:
                    print(log_info)

        return wrapper

    return decorator


@log()
def func(x, y):
    return str(x + y)

func(1, '2')