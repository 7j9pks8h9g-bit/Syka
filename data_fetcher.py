"""Отримання OHLCV-даних з публічного Binance Spot API (без ключа)."""
import requests
import pandas as pd

# Публічний домен Binance Market Data — альтернатива api.binance.com
BINANCE_URL = "https://data-api.binance.vision/api/v3/klines"


def fetch_klines(
    symbol: str = "BTCUSDT",
    interval: str = "5m",
    limit: int = 500
) -> pd.DataFrame:
    params = {
        "symbol": symbol.upper(),
        "interval": interval,
        "limit": min(max(int(limit), 1), 1000),
    }

    resp = requests.get(BINANCE_URL, params=params, timeout=20)
    resp.raise_for_status()

    raw = resp.json()
    if not raw:
        raise ValueError("Порожня відповідь від Binance API")

    df = pd.DataFrame(raw, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_volume", "trades",
        "taker_base", "taker_quote", "ignore",
    ])

    df["open_time"] = pd.to_datetime(
        df["open_time"], unit="ms", utc=True
    )

    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = df[col].astype(float)

    return df[
        ["open_time", "open", "high", "low", "close", "volume"]
    ]
