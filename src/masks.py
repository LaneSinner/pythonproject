import logging
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(
    LOG_DIR / "masks.log",
    mode="w",
    encoding="utf-8",
)

file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

file_handler.setFormatter(file_formatter)

if not logger.handlers:
    logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Функция, которая маскирует номер банковской карты."""
    logger.debug("Вызвана функция get_mask_card_number")

    try:
        if not card_number.isdigit() or len(card_number) < 4:
            raise ValueError("Некорректный номер карты")

        result = card_number[:4] + " " + card_number[4:6] + "** **** " + card_number[-4:]
        logger.info("Номер карты успешно замаскирован")
        return result

    except Exception:
        logger.exception("Ошибка при маскировке номера карты")
        raise


def get_mask_account(account_number: str) -> str:
    """Функция, которая маскирует номер банковского счёта."""
    logger.debug("Вызвана функция get_mask_account")
    try:
        if not account_number.isdigit() or len(account_number) < 4:
            raise ValueError("Некорректный номер счёта")

        result = "**" + account_number[-4:]
        logger.info("Номер счёта успешно замаскирован")
        return result

    except Exception:
        logger.exception("Ошибка при маскировке номера счёта")
        raise


if __name__ == "main":
    print(get_mask_card_number("7000792289606361"))
    print(get_mask_account("73654108430135874305"))
