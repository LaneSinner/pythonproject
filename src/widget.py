from masks import get_mask_card_number, get_mask_account

from datetime import datetime

def mask_account_card(card_or_account: str) -> str:
    """Маскирует номер карты или счета."""
    parts = card_or_account.split()
    number = parts[-1]

    if parts[0] == "Счет":
        masked_number = get_mask_account(number)
        return parts[0] + " " + masked_number
    else:
        masked_number = get_mask_card_number(number)
        return " ".join(parts[:-1]) + " " + masked_number


def get_date(date: str) -> str:
    """Преобразует дату в формат ДД.ММ.ГГГГ."""
    date_object = datetime.fromisoformat(date)
    return date_object.strftime("%d.%m.%Y")
