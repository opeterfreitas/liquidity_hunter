import pandas as pd
from typing import List, Literal
from config.constants import OB_BODY_RATIO_MIN

Direction = Literal['bullish', 'bearish']

class OrderBlockCandidate:
    def __init__(
        self,
        index: int,
        direction: Direction,
        open_price: float,
        close_price: float,
        high_price: float,
        low_price: float,
        breakout_confirmed: bool = False,
    ):
        self.index = index
        self.direction = direction
        self.open = open_price
        self.close = close_price
        self.high = high_price
        self.low = low_price
        self.breakout_confirmed = breakout_confirmed

    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "direction": self.direction,
            "open": self.open,
            "close": self.close,
            "high": self.high,
            "low": self.low,
            "breakout_confirmed": self.breakout_confirmed
        }

    def __repr__(self):
        return f"<OB {self.direction.upper()} | {self.open:.5f} → {self.close:.5f}>"

def detect_order_blocks(price_data: pd.DataFrame, body_ratio_min: float = OB_BODY_RATIO_MIN) -> List[OrderBlockCandidate]:
    """
    Detecta possíveis Order Blocks com base em padrões SMC.
    Espera um DataFrame com colunas ['open', 'high', 'low', 'close']
    """
    order_blocks = []

    for i in range(2, len(price_data) - 1):
        current = price_data.iloc[i]
        next_candle = price_data.iloc[i + 1]

        body = abs(current['close'] - current['open'])
        range_total = current['high'] - current['low']
        body_ratio = body / range_total if range_total > 0 else 0

        if body_ratio < body_ratio_min:
            continue  # vela com corpo muito fraco para OB

        # Detecta OB bullish (última vela bearish antes de alta forte)
        if current['close'] < current['open'] and next_candle['close'] > next_candle['open']:
            if next_candle['high'] > current['high']:
                order_blocks.append(
                    OrderBlockCandidate(
                        index=i,
                        direction='bullish',
                        open_price=current['open'],
                        close_price=current['close'],
                        high_price=current['high'],
                        low_price=current['low'],
                        breakout_confirmed=True
                    )
                )

        # Detecta OB bearish (última vela bullish antes de queda forte)
        elif current['close'] > current['open'] and next_candle['close'] < next_candle['open']:
            if next_candle['low'] < current['low']:
                order_blocks.append(
                    OrderBlockCandidate(
                        index=i,
                        direction='bearish',
                        open_price=current['open'],
                        close_price=current['close'],
                        high_price=current['high'],
                        low_price=current['low'],
                        breakout_confirmed=True
                    )
                )

    return order_blocks
