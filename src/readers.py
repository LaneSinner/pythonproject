from pathlib import Path
from typing import Any

import pandas as pd


def read_csv_file(file_path: str | Path) -> list[dict[str, Any]]:
    """Считывает финансовые операции из CSV-файла."""
    data = pd.read_csv(file_path)
    return data.to_dict(orient="records")


def read_excel_file(file_path: str | Path) -> list[dict[str, Any]]:
    """Считывает финансовые операции из Exce-файла."""
    data = pd.read_excel(file_path)
    return data.to_dict(orient="records")
