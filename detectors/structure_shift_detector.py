import pandas as pd
from typing import List, Literal
from config.constants import LOOKBACK_SWINGS_STRUCTURE, MIN_STRUCTURE_DISTANCE

BreakType = Literal['choch', 'mss']
Direction = Literal['bullish', 'bearish']

class StructureBreakEvent:
    def __init__(
        self,
        index: int,
        break_type: BreakType,
        direction: Direction,
        broken_level: float,
        close_price: float
    ):
        self.index = index
        self.break_type = break_type
        self.direction = direction
        self.broken_level = broken_level
        self.close_price = close_price

    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "break_type": self.break_type,
            "direction": self.direction,
            "broken_level": self.broken_level,
            "close_price": self.close_price
        }

    def __repr__(self):
        return f"<{self.break_type.upper()} {self.direction.upper()} @ {self.broken_level:.5f}>"

def detect_structure_breaks(price_data: pd.DataFrame, lookback: int = LOOKBACK_SWINGS_STRUCTURE) -> List[StructureBreakEvent]:
    """
    Detecta eventos de CHoCH ou MSS com base em swings anteriores.
    """
    structure_breaks = []

    for i in range(lookback, len(price_data)):
        current = price_data.iloc[i]
        close = current["close"]

        highs = price_data.iloc[i - lookback:i]["high"]
        lows = price_data.iloc[i - lookback:i]["low"]

        prev_high = highs.max()
        prev_low = lows.min()

        # Quebra de estrutura para baixo
        if close < prev_low and (prev_low - close) >= MIN_STRUCTURE_DISTANCE:
            structure_breaks.append(
                StructureBreakEvent(
                    index=i,
                    break_type="choch",
                    direction="bearish",
                    broken_level=prev_low,
                    close_price=close
                )
            )

        # Quebra de estrutura para cima
        elif close > prev_high and (close - prev_high) >= MIN_STRUCTURE_DISTANCE:
            structure_breaks.append(
                StructureBreakEvent(
                    index=i,
                    break_type="choch",
                    direction="bullish",
                    broken_level=prev_high,
                    close_price=close
                )
            )

    return structure_breaks
