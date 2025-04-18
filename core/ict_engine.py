from core.ict_utils import analyze_ict_structure
from telegram_bot.sender import send_signal_with_chart
from utils.logger import log_rodada


def generate_signals(symbol, timeframe, tipo="day"):
    try:
        result = analyze_ict_structure(symbol, timeframe)

        if not result or not isinstance(result, tuple) or len(result) != 4:
            log_rodada(tipo=tipo, analisados=1, gerados=0, ignorados=1, obs="Estrutura ICT inválida ou incompleta")
            return None

        signal, ohlcv, ote_zone, entry = result

        if not signal:
            log_rodada(tipo=tipo, analisados=1, gerados=0, ignorados=1, obs="Nenhum sinal retornado")
            return None

        signal.update({
            "symbol": symbol,
            "timeframe": timeframe
        })

        send_signal_with_chart(signal, ohlcv, ote_zone, entry)

        log_rodada(tipo=tipo, analisados=1, gerados=1, ignorados=0)

        return signal

    except Exception as e:
        log_rodada(tipo=tipo, analisados=1, gerados=0, ignorados=1, obs=f"Erro: {e}")
        return None
