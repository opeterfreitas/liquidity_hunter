import pandas as pd
from typing import List, Literal
from config.constants import FVG_MINIMUM_GAP_SIZE

Direction = Literal["bullish", "bearish"]

class FVGZoneCandidate:
    def __init__(
        self,
        index: int,
        direction: Direction,
        price_min: float,
        price_max: float,
        gap_size: float
    ):
        self.index = index
        self.direction = direction
        self.price_min = price_min
        self.price_max = price_max
        self.gap_size = gap_size

    def __repr__(self):
        return f"<FVG {self.direction.upper()} | {self.price_min:.5f} → {self.price_max:.5f}>"

    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "direction": self.direction,
            "price_min": self.price_min,
            "price_max": self.price_max,
            "gap_size": self.gap_size,
        }

def detect_fvg_zones(price_data: pd.DataFrame, minimum_gap_size: float = FVG_MINIMUM_GAP_SIZE) -> List[FVGZoneCandidate]:
    """
    Detecta zonas de Fair Value Gap.
    Espera um DataFrame com colunas ['open', 'high', 'low', 'close']
    """
    fvg_zones = []

    for i in range(2, len(price_data)):
        candle_prev = price_data.iloc[i - 2]
        candle_middle = price_data.iloc[i - 1]
        candle_next = price_data.iloc[i]

        # Bullish FVG: gap entre high anterior e low do próximo
        if candle_prev['high'] < candle_next['low']:
            gap = candle_next['low'] - candle_prev['high']
            if gap >= minimum_gap_size:
                fvg_zones.append(
                    FVGZoneCandidate(
                        index=i,
                        direction="bullish",
                        price_min=candle_prev['high'],
                        price_max=candle_next['low'],
                        gap_size=gap
                    )
                )

        # Bearish FVG: gap entre low anterior e high do próximo
        elif candle_prev['low'] > candle_next['high']:
            gap = candle_prev['low'] - candle_next['high']
            if gap >= minimum_gap_size:
                fvg_zones.append(
                    FVGZoneCandidate(
                        index=i,
                        direction="bearish",
                        price_min=candle_next['high'],
                        price_max=candle_prev['low'],
                        gap_size=gap
                    )
                )

    return fvg_zones
