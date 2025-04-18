# scanner/data.py

import requests
import time

def fetch_ohlcv(symbol: str, interval: str, limit: int = 100):
    url = f"https://fapi.binance.com/fapi/v1/klines"
    params = {
        "symbol": symbol.upper(),
        "interval": interval,
        "limit": limit,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        ohlcv = []
        for candle in data:
            ohlcv.append({
                "timestamp": candle[0],
                "open": float(candle[1]),
                "high": float(candle[2]),
                "low": float(candle[3]),
                "close": float(candle[4]),
                "volume": float(candle[5]),
            })

        return ohlcv

    except Exception as e:
        print(f"❌ Erro ao buscar OHLCV para {symbol} ({interval}): {e}")
        return []
