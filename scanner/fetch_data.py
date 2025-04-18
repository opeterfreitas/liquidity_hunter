import ccxt
import pandas as pd

exchange = ccxt.binance({
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future'
    }
})

def get_top_perpetuals(limit=400):
    markets = exchange.load_markets()
    perp_pairs = [
        symbol for symbol in markets
        if '/USDT' in symbol and markets[symbol].get('contractType') == 'PERPETUAL'
    ]

    tickers = exchange.fetch_tickers()
    volumes = [
        (symbol, tickers[symbol]['quoteVolume'])
        for symbol in perp_pairs if symbol in tickers
    ]

    volumes_sorted = sorted(volumes, key=lambda x: x[1], reverse=True)
    return [s[0].replace("/", "") for s in volumes_sorted[:limit]]

def get_ohlcv(symbol: str, timeframe='5m', limit=300):
    ohlcv = exchange.fetch_ohlcv(symbol.replace("USDT", "/USDT"), timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df
