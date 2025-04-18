from core.ict_engine import generate_signals
from core.ict_utils import analyze_ict_structure
from scanner.fetch_pairs import get_top_perpetuals
from telegram_bot.sender import send_signal_with_chart
from utils.logger import log_rodada
import traceback

SWING_TIMEFRAMES = ["4h", "1d"]

def generate_swing_signals():
    symbols = get_top_perpetuals(limit=400)

    total_analisados = 0
    total_gerados = 0
    total_ignorados = 0

    for symbol in symbols:
        for timeframe in SWING_TIMEFRAMES:
            print(f"🔍 [Swing] {symbol} - {timeframe}")
            try:
                result = analyze_ict_structure(symbol, timeframe)
                total_analisados += 1

                if result:
                    direction, ote_zone, entry, sl, tp, ohlcv = result
                    signal = {
                        "symbol": symbol,
                        "timeframe": timeframe,
                        "direction": direction,
                        "entry": entry,
                        "sl": sl,
                        "tp": tp,
                        "ote_min": ote_zone["min"],
                        "ote_max": ote_zone["max"],
                        "confidence": 0.8,
                        "confluences": "OTE + BOS",
                        "hit_tp": False,
                        "hit_sl": False,
                    }

                    generate_signals(signal, timeframe, tipo="swing")
                    send_signal_with_chart(signal, ohlcv, ote_zone, entry)
                    total_gerados += 1
                else:
                    print(f"⚠️ [Swing] Ignorado {symbol}-{timeframe}: estrutura incompleta")
                    total_ignorados += 1

            except Exception as e:
                print(f"❌ Erro ao enviar sinal/chart {symbol}-{timeframe}: {e}")
                traceback.print_exc()
                total_ignorados += 1

    log_rodada(tipo="swing", analisados=total_analisados, gerados=total_gerados, ignorados=total_ignorados, obs="Estrutura ICT inválida ou incompleta")
    print(f"✅ Finalizou Swing Trade com {total_analisados} analisados")
    return {
        "analisados": total_analisados,
        "gerados": total_gerados,
        "ignorados": total_ignorados
    }
