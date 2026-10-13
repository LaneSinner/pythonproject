import re
from collections import Counter
from typing import Any


def filter_by_state(
    operations: list[dict[str, Any]],
    state: str = "EXECUTED",
) -> list[dict[str, Any]]:
    """Фильтрует операции по статусу."""
    return [operation for operation in operations if operation.get("state") == state]


def sort_by_date(
    operations: list[dict[str, Any]],
    descending: bool = True,
) -> list[dict[str, Any]]:
    """Сортирует операции по дате."""
    return sorted(operations, key=lambda operation: operation["date"], reverse=descending)


def process_bank_search(data: list[dict[str, Any]], search: str) -> list[dict[str, Any]]:
    """Находит банковские операции, описание которых содержит поисковую строку."""
    if not search:
        return data.copy()

    pattern = re.compile(re.escape(search), re.IGNORECASE)

    return [operation for operation in data if pattern.search(str(operation.get("description", "")))]


def process_bank_operations(data: list[dict[str, Any]], categories: list[str]) -> dict[str, int]:
    """Подсчитывает количество банковских операций по заданным категориям."""
    description = Counter(operation.get("description", "") for operation in data)

    return {category: descriptions[category] for category in categories}
