import numpy as np
from datetime import datetime

from core.ict_tools import find_swing_points, detect_bos, calculate_ote, identify_ote_zone
from core.data_loader import get_ohlcv


def analyze_ict_structure(symbol, timeframe):
    print(f"🧠 Analisando estrutura ICT: {symbol}-{timeframe}")
    try:
        ohlcv = get_ohlcv(symbol, timeframe)

        if not ohlcv or len(ohlcv) < 5:
            print(f"⚠️ {symbol}-{timeframe}: OHLCV insuficiente ({len(ohlcv) if ohlcv else 0} candles)")
            return None

        ote_zone = identify_ote_zone(ohlcv)
        swing_highs, swing_lows = find_swing_points(ohlcv)
        direction, bos_index = detect_bos(ohlcv, swing_highs, swing_lows)

        if not direction or bos_index is None:
            print(f"⚠️ {symbol}-{timeframe}: BOS não encontrado")
            return None

        ote_min, ote_max, entry, sl, tp = calculate_ote(ohlcv, direction, bos_index)

        if any(val is None for val in [ote_min, ote_max, entry, sl, tp]):
            print(f"⚠️ {symbol}-{timeframe}: Cálculo OTE incompleto")
            return None

        print(f"✅ {symbol}-{timeframe}: Estrutura ICT válida detectada")
        return direction, {"min": float(ote_min), "max": float(ote_max)}, float(entry), float(sl), float(tp), ohlcv

    except Exception as e:
        print(f"❌ Erro ao analisar {symbol}-{timeframe}: {e}")
        return None


def identify_ote_zone(ohlcv: list):
    """
    Identifica a zona OTE (Optimal Trade Entry) com base nos últimos candles.
    Recebe uma lista de dicionários OHLCV e retorna um dicionário com os limites da OTE.
    """
    highs = [candle["high"] for candle in ohlcv]
    lows = [candle["low"] for candle in ohlcv]

    high = max(highs)
    low = min(lows)

    retracement_62 = low + (high - low) * 0.62
    retracement_79 = low + (high - low) * 0.79

    return {
        "min": min(retracement_62, retracement_79),
        "max": max(retracement_62, retracement_79)
    }
