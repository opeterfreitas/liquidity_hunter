# core/data_loader.py

from datetime import datetime, timedelta
import random

def get_ohlcv(symbol: str, timeframe: str, limit: int = 100) -> list[dict]:
    """
    Simula dados OHLCV no formato de lista de dicionários, com candles sintéticos.

    Parâmetros:
    - symbol: símbolo do ativo
    - timeframe: intervalo de tempo (ex: '1m', '5m', etc.)
    - limit: quantidade de candles a retornar

    Retorna:
    - Lista de candles no formato:
      {
          "timestamp": int,
          "open": float,
          "high": float,
          "low": float,
          "close": float,
          "volume": float
      }
    """
    now = datetime.utcnow()
    ohlcv = []

    for i in range(limit):
        timestamp = int((now - timedelta(minutes=limit - i)).timestamp())
        open_price = round(random.uniform(1, 100), 2)
        high_price = open_price + round(random.uniform(0, 5), 2)
        low_price = open_price - round(random.uniform(0, 5), 2)
        close_price = round(random.uniform(low_price, high_price), 2)
        volume = round(random.uniform(10, 1000), 2)

        candle = {
            "timestamp": timestamp,
            "open": open_price,
            "high": high_price,
            "low": low_price,
            "close": close_price,
            "volume": volume
        }

        ohlcv.append(candle)

    return ohlcv
