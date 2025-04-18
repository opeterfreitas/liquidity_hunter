from apscheduler.schedulers.background import BackgroundScheduler
from core.ict_engine import generate_signals
from core.validator import validate_signals, check_ote_touch
from ai.train_model import train_model
import time
import logging

logging.basicConfig(level=logging.INFO)

def run_generate():
    logging.info("⏱ Rodando geração de sinais ICT...")
    signals = generate_signals()
    logging.info(f"💡 {len(signals)} novos sinais gerados.")

def run_validate():
    logging.info("🔍 Validando TP/SL dos sinais...")
    validate_signals()

def run_ote_touch():
    logging.info("📍 Verificando toques em OTE...")
    check_ote_touch()

scheduler = BackgroundScheduler(timezone="UTC")

# Geração de sinais - análise de estrutura ICT
scheduler.add_job(run_generate, 'cron', hour='*', minute=0)

# Validação de TP e SL
scheduler.add_job(run_validate, 'interval', minutes=10)

# Verificação de toques em OTE (para entrada real)
scheduler.add_job(run_ote_touch, 'interval', minutes=10)

# Treino da IA 1x por dia (meia-noite UTC)
scheduler.add_job(train_model, 'cron', hour=0, minute=0)

scheduler.start()

print("✅ Scheduler iniciado. Pressione Ctrl+C para encerrar.")

try:
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
