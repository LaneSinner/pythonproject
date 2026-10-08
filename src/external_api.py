import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.apilayer.com/exchangerates_data/convert"


def convert_to_rub(transaction: dict[str, Any]) -> float:
    """Возвращает сумму транзакции в рублях."""

    amount = float(transaction["operationAmount"]["amount"])
    currency = transaction["operationAmount"]["currency"]["code"]

    if currency == "RUB":
        return amount

    api_key = os.getenv("EXCHANGE_RATES_API_KEY")

    if not api_key:
        raise ValueError("EXCHANGE_RATES_API_KEY is not set")

    params = {
        "from": currency,
        "to": "RUB",
        "amount": amount,
    }

    response = requests.get(
        API_URL,
        headers={"apikey": api_key},
        params=params,
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    if not data.get("success", False):
        raise RuntimeError(f"Conversion failed: {data}")

    if "result" not in data:
        raise RuntimeError("Currency conversion result is missing")

    return float(data["result"])
