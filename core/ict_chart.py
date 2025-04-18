import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import pandas as pd
import os

def generate_ict_chart(df: pd.DataFrame, signal: dict, save_path="chart.png"):
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plotagem dos candles (fechamento apenas para leveza)
    ax.plot(df['time'], df['close'], label='Close', color='black', linewidth=1)

    # Zona OTE
    ax.axhspan(signal['ote_min'], signal['ote_max'], color='blue', alpha=0.2, label='OTE Zone')

    # Entrada
    ax.axhline(signal['entry'], color='orange', linestyle='--', linewidth=1.5, label='Entry')

    # TP
    ax.axhline(signal['tp'], color='green', linestyle='--', linewidth=1.5, label='Take Profit')

    # SL
    ax.axhline(signal['sl'], color='red', linestyle='--', linewidth=1.5, label='Stop Loss')

    # BOS (opcional)
    if 'bos_time' in signal:
        bos_time = pd.to_datetime(signal['bos_time'], unit='ms')
        ax.axvline(bos_time, color='purple', linestyle=':', linewidth=1.2, label='BOS')

    # Legendas e títulos
    ax.legend(loc='upper left')
    ax.set_title(f"{signal['symbol']} - {signal['direction'].upper()} - {int(signal['confidence'] * 100)}%")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

    return save_path
