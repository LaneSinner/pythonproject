from collections.abc import Iterable, Iterator

from src.types import Transaction


def filter_by_currency(transactions: Iterable[Transaction], currency: str) -> Iterator[Transaction]:
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency:
            yield transaction


def transaction_descriptions(transactions: Iterable[Transaction]) -> Iterator[str]:
    for transaction in transactions:
        yield transaction["description"]
