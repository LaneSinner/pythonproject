import pytest

from src.processing import filter_by_state, sort_by_date, process_bank_operations, process_bank_search


@pytest.fixture
def operations():
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2024-03-11T02:26:18.671407",
        },
        {
            "id": 2,
            "state": "CANCELED",
            "date": "2024-01-15T10:20:30",
        },
        {
            "id": 3,
            "state": "EXECUTED",
            "date": "2024-01-20T12:00:00",
        },
    ]


@pytest.mark.parametrize(
    "state, expected_count",
    [
        ("EXECUTED", 2),
        ("CANCELED", 1),
    ],
)
def test_filter_by_state(operations, state, expected_count):
    result = filter_by_state(operations, state)

    assert len(result) == expected_count

    for operation in result:
        assert operation["state"] == state


def test_filter_by_state_no_matches(operations):
    result = filter_by_state(operations, "PENDING")

    assert result == []


def text_sort_by_date(operations):
    result = sort_by_date(operations)

    assert result[0]["date"] == "2024-03-11T02:26:18.671407"
    assert result[1]["date"] == "2024-01-15T10:20:30"
    assert result[2]["date"] == "2024-01-20T12:00:00"

    def test_process_bank_search() -> None:
        """Проверяет поиск операций по описанию."""

    data = [
        {"description": "Перевод организации"},
        {"description": "Оплата товаров"},
        {"description": "Перевод с карты на карту"},
    ]
    result = process_bank_search(data, "перевод")

    assert len(result) == 2
    assert result[0]["description"] == "Перевод организации"
    assert result[1]["description"] == "Перевод с карты на карту"

    def test_process_bank_search_no_matches() -> None:
        """Проверяет поиск, при котором совпадений нет."""

    data = [{"description": "Оплата товаров"}]
    assert process_bank_search(data, "перевод") == []

    def test_process_bank_search_case_insensitive() -> None:
        """Проверяет поиск без учёта регистра."""

    data = [{"description": "ПЕРЕВОД ОРГАНИЗАЦИИ"}]
    assert len(process_bank_search(data, "перевод")) == 1

    def test_process_bank_operations() -> None:
        """Проверяет подсчёт операций по категориям."""

    data = [
        {"description": "Перевод организации"},
        {"description": "Оплата товаров"},
        {"description": "Перевод организации"},
    ]
    result = process_bank_operations(
        data,
        ["Перевод организации", "Оплата товаров", "Переводы"],
    )

    assert result == {
        "Перевод организации": 2,
        "Оплата товаров": 1,
        "Переводы": 0,
    }

    def test_process_bank_operations_empty_data() -> None:
        """Проверяет подсчёт при пустом списке операций."""

    assert process_bank_operations([], ["Переводы"]) == {"Переводы": 0}
