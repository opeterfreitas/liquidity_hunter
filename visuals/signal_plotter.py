import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
import os
from config.settings import Settings
from datetime import datetime

def plot_signals(price_data: pd.DataFrame,
                 ote_zones=[],
                 ob_zones=[],
                 fvg_zones=[],
                 sweeps=[],
                 structure_breaks=[],
                 filename: str = "signal_preview") -> str:
    """
    Gera imagem dos sinais detectados em gráfico de candles com marcações.
    """

    fig, ax = plt.subplots(figsize=(12, 6))
    x = price_data.index
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Plotar candles
    for i in range(len(price_data)):
        open_price = price_data.iloc[i]["open"]
        close_price = price_data.iloc[i]["close"]
        high = price_data.iloc[i]["high"]
        low = price_data.iloc[i]["low"]

        color = "green" if close_price >= open_price else "red"
        ax.plot([i, i], [low, high], color="black", linewidth=0.5)
        ax.add_patch(plt.Rectangle((i - 0.3, min(open_price, close_price)),
                                   0.6,
                                   abs(open_price - close_price),
                                   color=color, alpha=0.8))

    # OTE Zones
    for zone in ote_zones:
        ax.axhspan(zone.zone_min_price, zone.zone_max_price, color='blue', alpha=0.2, label='OTE')

    # Order Blocks
    for ob in ob_zones:
        ax.axhspan(ob.low, ob.high, color='orange', alpha=0.2, label='OB')

    # FVG Zones
    for fvg in fvg_zones:
        ax.axhspan(fvg.price_min, fvg.price_max, color='purple', alpha=0.2, label='FVG')

    # Liquidity Sweeps
    for sweep in sweeps:
        color = "gold" if sweep.sweep_type == "high_sweep" else "brown"
        ax.plot(sweep.index, sweep.swept_level, marker="x", color=color, label=sweep.sweep_type.upper())

    # Structure Breaks
    for sb in structure_breaks:
        color = "blue" if sb.direction == "bullish" else "red"
        label = sb.break_type.upper()
        ax.plot(sb.index, sb.broken_level, marker="v", color=color, label=label)

    ax.set_title("Sinais Detectados")
    ax.set_ylabel("Preço")
    ax.set_xlabel("Índice de Candle")
    ax.grid(True)

    # Remover duplicatas de legendas
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='upper left')

    # Salvar imagem
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(Settings.OUTPUT_DIR, f"{filename}_{timestamp}.png")
    os.makedirs(Settings.OUTPUT_DIR, exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()

    return output_path
