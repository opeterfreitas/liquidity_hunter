import pandas as pd
from typing import List, Literal
from config.constants import FIB_61_8, FIB_79
from config.settings import Settings

Direction = Literal['bullish', 'bearish']

class OTEZoneCandidate:
    def __init__(
        self,
        swing_start_index: int,
        swing_end_index: int,
        direction: Direction,
        zone_min_price: float,
        zone_max_price: float
    ):
        self.swing_start_index = swing_start_index
        self.swing_end_index = swing_end_index
        self.direction = direction
        self.zone_min_price = zone_min_price
        self.zone_max_price = zone_max_price

    def __repr__(self):
        return f"<OTE {self.direction.upper()} | {self.zone_min_price:.5f} → {self.zone_max_price:.5f}>"

    def to_dict(self) -> dict:
        return {
            "start_index": self.swing_start_index,
            "end_index": self.swing_end_index,
            "direction": self.direction,
            "zone_min": self.zone_min_price,
            "zone_max": self.zone_max_price,
        }

def detect_ote_zones(price_data: pd.DataFrame, minimum_swing_size: float = Settings.MINIMUM_SWING_SIZE) -> List[OTEZoneCandidate]:
    ote_candidates = []

    for i in range(2, len(price_data)):
        candle_back = price_data.iloc[i - 2]
        candle_current = price_data.iloc[i]

        # Swing de alta
        if (
            candle_current["high"] > candle_back["high"] and
            candle_current["low"] > candle_back["low"]
        ):
            swing_high = candle_current["high"]
            swing_low = candle_back["low"]

            if (swing_high - swing_low) >= minimum_swing_size:
                zone_min = swing_high - FIB_79 * (swing_high - swing_low)
                zone_max = swing_high - FIB_61_8 * (swing_high - swing_low)
                ote_candidates.append(
                    OTEZoneCandidate(i - 2, i, 'bullish', zone_min, zone_max)
                )

        # Swing de baixa
        elif (
            candle_current["high"] < candle_back["high"] and
            candle_current["low"] < candle_back["low"]
        ):
            swing_high = candle_back["high"]
            swing_low = candle_current["low"]

            if (swing_high - swing_low) >= minimum_swing_size:
                zone_min = swing_low + FIB_61_8 * (swing_high - swing_low)
                zone_max = swing_low + FIB_79 * (swing_high - swing_low)
                ote_candidates.append(
                    OTEZoneCandidate(i - 2, i, 'bearish', zone_min, zone_max)
                )

    return ote_candidates
