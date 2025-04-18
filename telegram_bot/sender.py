import os
import matplotlib.pyplot as plt
from datetime import datetime
from io import BytesIO
import pandas as pd
import telegram

bot_token = os.getenv("TELEGRAM_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

bot = telegram.Bot(token=bot_token)

async def send_signal_with_chart(signal, ohlcv, ote_zone, entry):
    try:
        timestamps = [candle["timestamp"] for candle in ohlcv]
        closes = [candle["close"] for candle in ohlcv]

        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, closes, label='Preço', linewidth=2)

        plt.axhline(y=signal['entry'], color='blue', linestyle='--', label='Entry')
        plt.axhline(y=signal['tp'], color='green', linestyle='--', label='TP')
        plt.axhline(y=signal['sl'], color='red', linestyle='--', label='SL')
        plt.axhspan(ote_zone["min"], ote_zone["max"], color='orange', alpha=0.3, label='OTE')

        plt.title(f"{signal['symbol']} - {signal['direction'].upper()}")
        plt.xlabel("Timestamp")
        plt.ylabel("Preço")
        plt.legend()
        plt.grid(True)

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()

        message = (
            f"📈 Sinal detectado: {signal['symbol']} ({signal['timeframe']})\n"
            f"🔹 Direção: {signal['direction']}\n"
            f"🔹 Entry: {signal['entry']}\n"
            f"🔹 SL: {signal['sl']}\n"
            f"🔹 TP: {signal['tp']}\n"
            f"📊 Confluências: {signal['confluences']}\n"
            f"📈 Confiança: {signal['confidence'] * 100:.0f}%"
        )

        await bot.send_photo(chat_id=chat_id, photo=buffer, caption=message)
    except Exception as e:
        print(f"Erro ao enviar gráfico para {signal['symbol']}: {e}")