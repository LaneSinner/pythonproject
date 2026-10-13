from functools import wraps
from typing import Any, Callable


def log(filename: str | None = None) -> Callable:
    """Декоратор для логирования выполнения функции.

    :param filename: Имя файла для записи логов. Если None, вывод идет в консоль.
    """

    def my_decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)

                log_message = f"{func.__name__} ok"

                _write_log(log_message, filename)

                return result

            except Exception as e:
                error_name = e.__class__.__name__
                log_message = f"{func.__name__} error: {error_name}. Inputs: {args}, {kwargs}"

                _write_log(log_message, filename)

                raise e

        return wrapper

    return my_decorator


def _write_log(message: str, filename: str | None) -> None:
    """Записывает сообщение в файл или выводит его в консоль."""
    if filename:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    else:
        print(message)
