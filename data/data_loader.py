import requests
import pandas as pd
from datetime import datetime

TIMEFRAME_BINANCE_MAP = {
    "M1": "1m",
    "M5": "5m",
    "M15": "15m",
    "H1": "1h",
    "H4": "4h",
    "D1": "1d"
}

def load_price_data(pair: str, timeframe: str, limit: int = 100) -> pd.DataFrame:
    """
    Carrega candles da Binance e retorna DataFrame com colunas ['open', 'high', 'low', 'close']
    """
    tf_binance = TIMEFRAME_BINANCE_MAP.get(timeframe.upper())
    if not tf_binance:
        raise ValueError(f"Timeframe {timeframe} inválido.")

    url = f"https://api.binance.com/api/v3/klines?symbol={pair}&interval={tf_binance}&limit={limit}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    df = pd.DataFrame(data, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
    ])

    df = df[["open", "high", "low", "close"]].astype(float)
    return df
