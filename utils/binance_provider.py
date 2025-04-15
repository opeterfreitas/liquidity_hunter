import requests
from datetime import datetime

TIMEFRAME_BINANCE_MAP = {
    "M1": "1m",
    "M5": "5m",
    "M15": "15m",
    "H1": "1h",
    "H4": "4h",
    "D1": "1d"
}

def get_latest_candle_time(pair: str, timeframe: str) -> str:
    tf_binance = TIMEFRAME_BINANCE_MAP.get(timeframe.upper())
    if not tf_binance:
        raise ValueError(f"Timeframe {timeframe} inválido.")

    url = f"https://api.binance.com/api/v3/klines?symbol={pair}&interval={tf_binance}&limit=1"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    if not data or len(data[0]) < 1:
        raise ValueError(f"Nenhum candle encontrado para {pair} {timeframe}")

    open_time_ms = data[0][0]
    open_time_dt = datetime.utcfromtimestamp(open_time_ms / 1000.0)
    return open_time_dt.isoformat() + "Z"
