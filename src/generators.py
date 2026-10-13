from collections.abc import Iterable, Iterator

from src.types import Transaction


def filter_by_currency(transactions: Iterable[Transaction], currency: str) -> Iterator[Transaction]:
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency:
            yield transaction


def transaction_descriptions(transactions: Iterable[Transaction]) -> Iterator[str]:
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start, stop):
    for number in range(start, stop + 1):
        card_number = str(number).zfill(16)
        yield f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}"
