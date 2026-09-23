import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def operations():
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2024-03-11T02:26:18.671407",
        },
        {
            "id": 2,
            "state": "CANCELED",
            "date": "2024-01-15T10:20:30",
        },
        {
            "id": 3,
            "state": "EXECUTED",
            "date": "2024-01-20T12:00:00",
        },
    ]


@pytest.mark.parametrize(
    "state, expected_count",
    [
        ("EXECUTED", 2),
        ("CANCELED", 1),
    ],
)
def test_filter_by_state(operations, state, expected_count):
    result = filter_by_state(operations, state)

    assert len(result) == expected_count

    for operation in result:
        assert operation["state"] == state


def test_filter_by_state_no_matches(operations):
    result = filter_by_state(operations, "PENDING")

    assert result == []


def text_sort_by_date(operations):
    result = sort_by_date(operations)

    assert result[0]["date"] == "2024-03-11T02:26:18.671407"
    assert result[1]["date"] == "2024-01-15T10:20:30"
    assert result[2]["date"] == "2024-01-20T12:00:00"
