"""Fixed-rate currency conversion. The base currency for generated costs is USD."""

_RATES = {
    "USD": 1.0,
    "INR": 83.0,
    "AED": 3.67,
    "EUR": 0.92,
    "GBP": 0.79,
}

_SYMBOLS = {
    "USD": "$",
    "INR": "₹",
    "AED": "AED",
    "EUR": "€",
    "GBP": "£",
}


def convert_currency(amount: float, to_currency: str = "USD") -> tuple[float, str]:
    rate = _RATES.get(to_currency, 1.0)
    return amount * rate, _SYMBOLS.get(to_currency, "$")
