from utils.candle_control import candle_is_new
from your_data_provider import get_latest_candle_time  # (você definirá isso)

def run_all_pairs_all_timeframes():
    pairs = get_active_pairs()
    for pair in pairs:
        for tf in TIMEFRAMES:
            # Você precisará obter o timestamp do último candle de fato (da sua fonte de dados)
            latest_candle_time = get_latest_candle_time(pair, tf)

            if candle_is_new(pair, tf, latest_candle_time):
                run_signal_pipeline_for_pair_timeframe(pair, tf)
