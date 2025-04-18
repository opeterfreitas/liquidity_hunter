# core/validator.py

from db.repository import SessionLocal
from db.models import Signal
from telegram_bot.sender import send_signal_with_chart
from scanner.data import fetch_ohlcv


def validate_signals():
    session = SessionLocal()
    signals = session.query(Signal).filter_by(hit_tp=False, hit_sl=False).all()

    for signal in signals:
        try:
            ohlcv = fetch_ohlcv(signal.symbol, signal.timeframe)
            latest_price = ohlcv[-1]["close"]

            # Detectar toque na OTE
            if signal.ote_min <= latest_price <= signal.ote_max:
                send_signal_with_chart(signal, ohlcv, evento="toque_ote")

            # Detectar TP atingido
            if (signal.direction == "buy" and latest_price >= signal.tp) or \
                    (signal.direction == "sell" and latest_price <= signal.tp):
                signal.hit_tp = True
                session.commit()
                send_signal_with_chart(signal, ohlcv, evento="tp_atingido")

            # Detectar SL (se quiser adicionar também)
            if (signal.direction == "buy" and latest_price <= signal.sl) or \
                    (signal.direction == "sell" and latest_price >= signal.sl):
                signal.hit_sl = True
                session.commit()
                # Opcional: envio de alerta de SL

        except Exception as e:
            print(f"❌ Erro ao validar {signal.symbol}: {e}")

    session.close()
