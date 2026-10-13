import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "value, expected",
    [
        (
            "Visa Platinum 1234567812345678",
            "Visa Platinum 1234 56** **** 5678",
        ),
        (
            "Счет 12345678901234567890",
            "Счет **7890",
        ),
    ],
)
def test_mask_account_card(value, expected):
    assert mask_account_card(value) == expected


@pytest.mark.parametrize(
    "date, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2024-01-15T10:20:30", "15.01.2024"),
    ],
)
def test_get_date(date, expected):
    assert get_date(date) == expected
