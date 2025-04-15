import pandas as pd
from typing import List, Literal
from config.constants import LOOKBACK_CANDLES_SWEEP, SWEEP_TOLERANCE_PIPS

SweepType = Literal['high_sweep', 'low_sweep']

class LiquiditySweepCandidate:
    def __init__(
        self,
        index: int,
        sweep_type: SweepType,
        swept_level: float,
        sweep_candle_high: float,
        sweep_candle_low: float,
        distance: float
    ):
        self.index = index
        self.sweep_type = sweep_type
        self.swept_level = swept_level
        self.sweep_candle_high = sweep_candle_high
        self.sweep_candle_low = sweep_candle_low
        self.distance = distance

    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "sweep_type": self.sweep_type,
            "swept_level": self.swept_level,
            "sweep_high": self.sweep_candle_high,
            "sweep_low": self.sweep_candle_low,
            "distance": self.distance,
        }

    def __repr__(self):
        return f"<SWEEP {self.sweep_type.upper()} @ {self.swept_level:.5f} | Δ={self.distance:.5f}>"

def detect_liquidity_sweeps(price_data: pd.DataFrame, lookback: int = LOOKBACK_CANDLES_SWEEP) -> List[LiquiditySweepCandidate]:
    """
    Detecta sweeps de liquidez (altas ou mínimas varridas).
    """
    sweeps = []

    for i in range(lookback, len(price_data)):
        current = price_data.iloc[i]
        highs = price_data.iloc[i - lookback:i]["high"]
        lows = price_data.iloc[i - lookback:i]["low"]

        max_prev = highs.max()
        min_prev = lows.min()

        # Sweep de alta (alta anterior foi rompida e rejeitada)
        if current["high"] > max_prev and current["close"] < max_prev:
            diff = current["high"] - max_prev
            if diff >= SWEEP_TOLERANCE_PIPS:
                sweeps.append(
                    LiquiditySweepCandidate(
                        index=i,
                        sweep_type="high_sweep",
                        swept_level=max_prev,
                        sweep_candle_high=current["high"],
                        sweep_candle_low=current["low"],
                        distance=diff
                    )
                )

        # Sweep de baixa (mínima anterior foi rompida e rejeitada)
        if current["low"] < min_prev and current["close"] > min_prev:
            diff = min_prev - current["low"]
            if diff >= SWEEP_TOLERANCE_PIPS:
                sweeps.append(
                    LiquiditySweepCandidate(
                        index=i,
                        sweep_type="low_sweep",
                        swept_level=min_prev,
                        sweep_candle_high=current["high"],
                        sweep_candle_low=current["low"],
                        distance=diff
                    )
                )

    return sweeps
