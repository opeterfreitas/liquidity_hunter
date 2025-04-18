# core/ict_tools.py

import pandas as pd


def find_swing_points(ohlcv):
    swing_highs = []
    swing_lows = []
    for i in range(2, len(ohlcv) - 2):
        if ohlcv[i]["high"] > ohlcv[i - 1]["high"] and ohlcv[i]["high"] > ohlcv[i + 1]["high"]:
            swing_highs.append((i, ohlcv[i]["high"]))
        if ohlcv[i]["low"] < ohlcv[i - 1]["low"] and ohlcv[i]["low"] < ohlcv[i + 1]["low"]:
            swing_lows.append((i, ohlcv[i]["low"]))
    return swing_highs, swing_lows


def detect_bos(ohlcv, swing_highs, swing_lows):
    if not swing_highs or not swing_lows:
        return None, None

    last_high_idx, last_high = swing_highs[-1]
    last_low_idx, last_low = swing_lows[-1]
    current_price = ohlcv[-1]["close"]

    if current_price > last_high:
        return "buy", last_high_idx
    elif current_price < last_low:
        return "sell", last_low_idx
    else:
        return None, None


def calculate_ote(ohlcv, direction, bos_index):
    last = ohlcv[bos_index]

    if direction == "buy":
        low = last["low"]
        high = last["high"]
    else:
        high = last["high"]
        low = last["low"]

    retracement_range = high - low
    ote_min = low + retracement_range * 0.62
    ote_max = low + retracement_range * 0.79

    entry_price = (ote_min + ote_max) / 2
    sl = entry_price * (0.98 if direction == "buy" else 1.02)
    tp = entry_price * (1.04 if direction == "buy" else 0.96)

    return round(ote_min, 8), round(ote_max, 8), round(entry_price, 8), round(sl, 8), round(tp, 8)


def identify_ote_zone(ohlcv):
    try:
        highs = [candle["high"] for candle in ohlcv]
        lows = [candle["low"] for candle in ohlcv]
        high = max(highs)
        low = min(lows)
        diff = high - low
        ote_min = low + diff * 0.62
        ote_max = low + diff * 0.79
        return round(ote_min, 8), round(ote_max, 8)
    except Exception as e:
        print(f"Erro ao identificar zona OTE: {e}")
        return None, None
