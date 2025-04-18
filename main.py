from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time
import threading
import traceback

from core.day_trade import generate_day_signals
from core.swing_trade import generate_swing_signals
from core.validator import validate_signals
from core.train import train_ai_day, train_ai_swing
from db.init_db import init_db

# Variáveis globais para totalização
total_analised = 0
total_generated = 0
total_ignored = 0

# Flags para status
is_running = False


def run_day_and_swing():
    global total_analised, total_generated, total_ignored, is_running

    try:
        is_running = True
        print("\n🔎 Iniciando rodada completa (Day + Swing)...")

        start = time.time()

        # Day trade
        print("📈 Iniciando sinais Day Trade...")
        start_day = time.time()
        day_result = generate_day_signals()
        print(f"✅ Finalizou Day Trade em {round(time.time() - start_day, 2)}s")

        # Swing trade
        print("📉 Iniciando sinais Swing Trade...")
        start_swing = time.time()
        swing_result = generate_swing_signals()
        print(f"✅ Finalizou Swing Trade em {round(time.time() - start_swing, 2)}s")

        # Totalizador
        total_analised = day_result["analisados"] + swing_result["analisados"]
        total_generated = day_result["gerados"] + swing_result["gerados"]
        total_ignored = day_result["ignorados"] + swing_result["ignorados"]

        print("\n📊 Totalizador da Rodada:")
        print(f"   - 🔍 Sinais analisados: {total_analised}")
        print(f"   - ✅ Sinais gerados: {total_generated}")
        print(f"   - ⚠️ Sinais ignorados: {total_ignored}")

        print(f"🕒 Rodada completa finalizada em {round(time.time() - start, 2)}s")
        print("⏳ Aguardando próxima rodada...\n")

        # Executa validação imediatamente após
        print("🔎 Iniciando Validação de Sinais (pós-rodada)...")
        start_val = time.time()
        validate_signals()
        print(f"✅ Validação finalizada em {round(time.time() - start_val, 2)}s")

    except Exception as e:
        print("❌ Erro durante a execução da rodada:")
        traceback.print_exc()
    finally:
        is_running = False


def start_system():
    print("🔧 Inicializando banco de dados (init_db)...")
    init_db()
    print("🚀 Iniciando Liquidity Hunter com modelo híbrido (Day + Swing)...\n")

    scheduler = BackgroundScheduler(timezone="UTC", daemon=True)

    # Rodada híbrida a cada 10 minutos
    scheduler.add_job(run_day_and_swing, 'interval', minutes=10, id='run_all', max_instances=1, coalesce=True)

    # Treinamento diário das IAs
    scheduler.add_job(train_ai_day, 'cron', hour=0, minute=0, id='train_ai_day')
    scheduler.add_job(train_ai_swing, 'cron', hour=0, minute=5, id='train_ai_swing')

    scheduler.start()

    # Primeira rodada logo ao iniciar
    threading.Thread(target=run_day_and_swing).start()

    try:
        while True:
            status = "🔄 Sistema analisando sinais..." if is_running else "⏳ Aguardando próxima rodada..."
            print(f"[{datetime.utcnow().strftime('%H:%M:%S')}] {status}")
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        print("⛔ Encerrando Liquidity Hunter...")
        scheduler.shutdown()


if __name__ == "__main__":
    start_system()
