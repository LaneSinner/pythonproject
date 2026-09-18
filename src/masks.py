def get_mask_card_number(card_number:str) -> str:
    """Функция которая маскирует номера банковской карты"""
    return card_number[:4] + " " + card_number[4:6] + "** **** " + card_number[-4:]


def get_mask_account(account_number:str) -> str:
    """Функция которая маскирует номера банковского счета"""
    return "**" + account_number[-4:]


if __name__ == "__main__":
    print(get_mask_card_number("7000792289606361"))
    print(get_mask_account("73654108430135874305"))