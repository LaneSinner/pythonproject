import json
import logging
from pathlib import Path
from typing import Any

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(
    LOG_DIR / "utils.log",
    mode="w",
    encoding="utf-8",
)

file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

file_handler.setFormatter(file_formatter)

if not logger.handlers:
    logger.addHandler(file_handler)


def read_json_file(file_path: str | Path) -> list[dict[str, Any]]:
    """Читает список транзакций из JSON-файла."""
    logger.debug("Начато чтение JSON-файла: %s", file_path)

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            logger.error("Содержимое JSON-файла не является списком")
            return []

        logger.info("JSON-файл успешно прочитан: %s", file_path)
        return data

    except (FileNotFoundError, json.JSONDecodeError, OSError):
        logger.exception("Ошибка при чтении JSON-файла: %s", file_path)
        return []
