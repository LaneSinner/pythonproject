import json
from pathlib import Path
from typing import Any


def read_json_file(file_path: str | Path) -> list[dict[str, Any]]:
    """Читает список транзакций из JSON-файла."""

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    if not isinstance(data, list):
        return []

    return data
