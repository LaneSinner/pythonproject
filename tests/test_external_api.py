from unittest.mock import Mock, patch

import pytest

from src.external_api import convert_to_rub


@pytest.fixture
def usd_transaction():
    return {
        "operationAmount": {
            "amount": "100.00",
            "currency": {
                "code": "USD",
                "name": "USD",
            },
        }
    }


def test_convert_rub_transaction():
    transaction = {
        "operationAmount": {
            "amount": "1234.56",
            "currency": {
                "code": "RUB",
                "name": "руб.",
            },
        }
    }
    assert convert_to_rub(transaction) == 1234.56


@patch("src.external_api.requests.get")
@patch.dict(
    "os.environ",
    {"EXCHANGE_RATES_API_KEY": "test-key"},
)
def test_convert_usd_transaction(
    mock_get: Mock,
    usd_transaction: dict,
):
    mock_response = Mock()

    mock_response.json.return_value = {
        "success": True,
        "result": 9200.0,
    }

    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    result = convert_to_rub(usd_transaction)

    assert result == 9200.0

    mock_get.assert_called_once()

    assert mock_get.call_args.kwargs["headers"] == {"apikey": "test-key"}

    assert mock_get.call_args.kwargs["params"] == {
        "from": "USD",
        "to": "RUB",
        "amount": 100.0,
    }


@patch("src.external_api.requests.get")
@patch.dict(
    "os.environ",
    {"EXCHANGE_RATES_API_KEY": "test-key"},
)
def test_convert_api_error(
    mock_get: Mock,
    usd_transaction: dict,
):
    mock_response = Mock()

    mock_response.raise_for_status.side_effect = RuntimeError(
        "API error"
    )

    mock_get.return_value = mock_response

    with pytest.raises(RuntimeError, match="API error"):
        convert_to_rub(usd_transaction)


@patch.dict("os.environ", {}, clear=True)
def test_convert_without_api_key(usd_transaction: dict):
    with pytest.raises(
        ValueError,
        match="EXCHANGE_RATES_API_KEY",
    ):
        convert_to_rub(usd_transaction)
