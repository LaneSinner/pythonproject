import pytest

from src.decorators import log


def test_log_console_success(capsys: pytest.CaptureFixture) -> None:
    """Проверяет усспешное выполнение с выводом в консоль."""

    @log()
    def add(x: int, y: int) -> int:
        return x + y

    result = add(2, 3)

    assert result == 5
    captured = capsys.readouterr()
    assert "add ok" in captured.out


def test_log_console_error(capsys: pytest.CaptureFixture) -> None:
    """Проверяет логирования ошибки в консоль."""

    @log()
    def divide(x: int, y: int) -> float:
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    captured = capsys.readouterr()
    assert "divide error: ZeroDivisionError" in captured.out
    assert "Inputs: (1, 0)" in captured.out


def test_log_file_success(tmp_path: pytest.TempPathFactory) -> None:
    """Проверяет запись успешного выполнения в файл."""
    log_file = tmp_path / "test_log.txt"

    @log(filename=str(log_file))
    def multiply(x: int, y: int) -> int:
        return x * y

    result = multiply(3, 4)

    assert result == 12
    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert "multiply ok" in content


def test_log_file_error(tmp_path: pytest.TempPathFactory) -> None:
    """Проверяет запись ошибки в файл."""
    log_file = tmp_path / "test_log.txt"

    @log(filename=str(log_file))
    def bad_func() -> None:
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        bad_func()

    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert "bad_func error: ValueError" in content
    assert "Inputs: ()" in content
